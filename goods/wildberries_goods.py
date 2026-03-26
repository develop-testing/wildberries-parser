from __future__ import annotations
from dataclasses import dataclass
from DrissionPage import SessionPage  # type: ignore
from promise import Promise
from time import sleep

from .goods import Goods
from .goods import GoodsPrint
from .base_goods import GoodsOfhQuery


@dataclass(slots=True)
class WildberriesGoods(Goods):
    origin: Goods
    x_wbaas_token: str

    def __post_init__(self) -> None:
        if len(self.x_wbaas_token) > 600:
            raise ValueError("second table name is too long")

    def query(self) -> str:
        return self.origin.query()

    def print(self, page_start: int, page_end: int) -> GoodsPrint:
        query = self.origin.query()
        products = []
        page_number = page_start
        max_pages = page_end

        page = SessionPage()

        page.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Referer": "https://www.wildberries.ru",
                "Accept": "*/*",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            }
        )

        page.session.cookies.update({"x_wbaas_token": self.x_wbaas_token})

        while page_number <= max_pages:
            page.get(
                "https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-5818883&hide_vflags=4294967296&lang=ru&page="
                + str(page_number)
                + "&query="
                + str(query)
                + "&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
            )

            json_result = page.json

            if not "products" in json_result:
                break

            for item in page.json["products"]:
                products.append(item["id"])

            page_number += 1

        self.origin = GoodsOfhQuery(query, products)
        
        return self.origin.print(page_start, page_end)

    @staticmethod
    def new(query: str, x_wbaas_token: str) -> WildberriesGoods:
        return WildberriesGoods(GoodsOfhQuery(query, []), x_wbaas_token)
