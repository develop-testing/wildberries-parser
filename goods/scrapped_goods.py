from __future__ import annotations
from dataclasses import dataclass
from DrissionPage import ChromiumPage, ChromiumOptions
from promise import Promise

from .goods import Goods
from .goods import GoodsPrint
from .goods_of_query import GoodsOfhQuery


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
                    GoodsOfhQuery(query, [])
                )
            )
        )