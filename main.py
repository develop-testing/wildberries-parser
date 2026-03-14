from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass
from promise import Promise

from DrissionPage import ChromiumPage, ChromiumOptions


@dataclass(slots=True)
class ProductPrint:
    descr: str
    images: list[str]
    characters: list[str]
    raiting: int
    reviews_count: int
    link: str
    articul: str
    name: str
    price: str
    seller_name: str
    seller_link: str
    sizes: list[str]
    quantity: int


@dataclass(slots=True)
class GoodsPrint:
    query: str
    count: int
    products: str


class Goods(Protocol):
    def print(self) -> GoodsPrint:
        pass


@dataclass(slots=True, frozen=True)
class GoodsOfSearchQuery(Goods):
    query: str
    products: list[int]

    def __post_init__(self):
        if len(self.query) > 500:
            raise ValueError("query of goods is too long")
        
        if not isinstance(self.query, str):
            raise ValueError("query of goods is not string")
        
        if self.products:
            for value in self.products:
                if not isinstance(value, int):
                    raise ValueError("product id is not int")

                if len(value) > 256:
                    raise ValueError("product id is too long")


    def print(self) -> GoodsPrint:
        printout = GoodsPrint(
            query=self.query,
            count=len(self.data),
            products=self.products
        )

        return printout


@dataclass(slots=True, frozen=True)
class WildberriesScrappedGoods(Goods):
    origin: Goods

    def print(self) -> GoodsPrint:
        return self.origin.print()

    @staticmethod
    def new(query: str) -> Promise[WildberriesScrappedGoods]:
        def executor(resolve, reject):
            options = ChromiumOptions()
            options.headless(True)  # Это скроет окно браузера
            page = ChromiumPage(addr_or_opts=options)

            url = "https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-5818883&hide_vflags=4294967296&lang=ru&page=1&query=пальто из натуральной шерсти&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"

            try:
                page.get(url)

                items = page.json["products"]

                for item in items:
                    print(item)
                    break
            finally:
                page.quit()

        return (
            Promise(executor)
            .then(lambda data:
                WildberriesScrappedGoods(
                    GoodsOfSearchQuery(query, [])
                )
            )
        )


WildberriesScrappedGoods\
    .new("пальто из натуральной шерсти")\
    .then(lambda goods: goods.print())\
    .then(print)\
    .catch(print)