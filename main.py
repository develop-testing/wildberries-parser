from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass
from promise import Promise
import requests


@dataclass(slots=True)
class ProductPrint:
    link: str
    name: str


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
    data: list[dict[str, str]]

    def __post_init__(self):
        if len(self.query) > 500:
            raise ValueError("query of goods is too long")
        
        if not isinstance(self.query, str):
            raise ValueError("query of goods is not string")
        
        if self.data:
            for item in self.data:
                for value in item.values():
                    if not isinstance(value, str):
                        raise ValueError("value of goods is not string")

                    if len(value) > 3000:
                        raise ValueError("value of goods items is too long")


    def print(self) -> GoodsPrint:
        printout = GoodsPrint(
            query=self.query,
            count=len(self.data),
            products=[]
        )

        for item in self.data:
            printout.products.append(
                ProductPrint(
                    link=item['link'],
                    articul=item['articul'],
                    name=item['name'],
                    price=item['price'],
                )
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
            try:
                data = requests.get(
                    "https://www.wildberries.ru/catalog/444246710/detail.aspx",
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'DNT': '1',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-User': '?1',
                        'Cache-Control': 'max-age=0',
                    }
                ).text
                print(data)
            except Exception as e:
                reject(e)

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