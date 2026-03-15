from __future__ import annotations
from dataclasses import dataclass
from DrissionPage import ChromiumPage, ChromiumOptions  # type: ignore
from promise import Promise
from time import sleep

from .goods import Goods
from .goods import GoodsPrint
from .goods_of_query import GoodsOfhQuery


@dataclass(slots=True)
class WildberriesScrappedGoods(Goods):
    origin: Goods

    def query(self) -> str:
        return self.origin.query()

    def print(self) -> GoodsPrint:
        try:
            query = self.origin.query()
            products = []
            page_number = 1
            max_pages = 999

            options = ChromiumOptions()
            options.headless(True)  # hide window
            web_page = ChromiumPage(addr_or_opts=options)

            while page_number <= max_pages:
                web_page.get(
                    "https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-5818883&hide_vflags=4294967296&lang=ru&page="
                    + str(page_number)
                    + "&query="
                    + str(query)
                    + "&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
                )

                json_result = web_page.json

                if not "products" in json_result:
                    break

                for item in web_page.json["products"]:
                    products.append(item["id"])

                page_number += 1

                sleep(0.5)

            self.origin = GoodsOfhQuery(query, products)

        finally:
            web_page.quit()

        return self.origin.print()

    @staticmethod
    def new(query: str) -> WildberriesScrappedGoods:
        return WildberriesScrappedGoods(GoodsOfhQuery(query, []))
