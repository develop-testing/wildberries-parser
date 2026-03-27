from __future__ import annotations
from dataclasses import dataclass
from DrissionPage import SessionPage  # type: ignore

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

    def fetch(self, from_number: int, count: int) -> GoodsPrint:
        result = self.origin.fetch(1, 999)

        if not result.products:
            query = self.origin.query()
            items_on_page = 0
            products = []

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

            page.get(f"https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-5818883&hide_vflags=4294967296&lang=ru&page=1&query=${query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false")

            json_result = page.json

            items_on_page = len(json_result["products"])
            
            start_page = from_number // items_on_page + 1
            end_page = (from_number + count - 1) // items_on_page + 1
            page_num = start_page

            start_index = from_number % items_on_page
            end_index = (from_number + count - 1) % items_on_page + 1

            print(page_num)

            while page_num <= end_page:
                page.get(f"https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-5818883&hide_vflags=4294967296&lang=ru&page=${page_num}&query=${query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false")
                
                json_result = page.json
                page_products = json_result.get("products", [])
                
                if page_num == start_page and page_num == end_page:
                    # Одна страница
                    products.extend([p.get("id") for p in page_products[start_index:start_index + count]])
                elif page_num == start_page:
                    # Первая страница
                    products.extend([p.get("id") for p in page_products[start_index:]])
                elif page_num == end_page:
                    # Последняя страница
                    products.extend([p.get("id") for p in page_products[:end_index]])
                else:
                    # Промежуточные страницы
                    products.extend([p.get("id") for p in page_products])
                
                page_num += 1

            self.origin = GoodsOfhQuery(query, products)

        return self.origin.fetch(1, 999)

    @staticmethod
    def new(query: str, x_wbaas_token: str) -> WildberriesGoods:
        return WildberriesGoods(GoodsOfhQuery(query, []), x_wbaas_token)
