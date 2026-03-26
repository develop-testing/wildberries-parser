from __future__ import annotations
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dataclasses import dataclass
from html_page.mstache_html_page import MstacheHtmlPage
from product.fk_product import FakeProduct
from product.wildberries_product import WildberriesProduct
from goods.wildberries_goods import WildberriesGoods

app = FastAPI()


from typing import Protocol


class TempAuthoTokens(Protocol):
    def value(self) -> str:
        pass


@dataclass(frozen=True, slots=True)
class TempAuthoToken(TempAuthoTokens):
    content: str

    def __post_init__(self) -> None:
        if len(self.content) > 1024 or len(self.content) < 50:
            raise ValueError("incorect size of temp auth token")

    def value(self) -> str:
        return self.content


from DrissionPage import ChromiumPage, ChromiumOptions  # type: ignore[import-untyped]


@dataclass(slots=True)
class WBTempAuthoToken(TempAuthoTokens):
    origin: TempAuthoTokens | None

    def value(self) -> str:
        if not self.origin:
            co = ChromiumOptions()
            co.headless()  # Enable headless mode
            co.set_argument("--disable-gpu")
            co.set_argument("--no-sandbox")
            co.set_argument("--window-size=1920,1080")
            co.set_argument("--disable-blink-features=AutomationControlled")

            page = ChromiumPage(co)

            page.set.headers(
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "Cache-Control": "max-age=0",
                }
            )

            page.get("https://www.wildberries.ru/")

            cookies = page.cookies()

            value = ""

            for cookie in cookies:
                if cookie["name"] == "x_wbaas_token":
                    value = cookie["value"]

            self.origin = TempAuthoToken(value)

        return self.origin.value()

    @staticmethod
    def new() -> WBTempAuthoToken:
        return WBTempAuthoToken(None)


import os
from datetime import datetime, timedelta


@dataclass(slots=True)
class CachedTempAuthoToken(TempAuthoTokens):
    origin: TempAuthoTokens
    file_path: str
    expired_seconds: int

    def _fetch_and_save(self) -> str:
        value = self.origin.value()

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(value)

        return value

    def value(self) -> str:
        if not os.path.exists(self.file_path):
            return self._fetch_and_save()

        file_mtime = os.path.getmtime(self.file_path)
        file_time = datetime.fromtimestamp(file_mtime)
        current_time = datetime.now()

        if current_time - file_time > timedelta(seconds=self.expired_seconds):
            return self._fetch_and_save()

        with open(self.file_path, "r", encoding="utf-8") as f:
            value = f.read().strip()

        return value

    def new(
        origin: TempAuthoTokens, file_path: str, expired_seconds: int
    ) -> CachedTempAuthoToken:
        return CachedTempAuthoToken(origin, file_path, expired_seconds)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, query: str = "", marketplace: list[str] = []) -> str:
    products: list[FakeProduct] = []

    if "wildberries" in marketplace:
        goods_query = WildberriesGoods.new(
            query,
            CachedTempAuthoToken.new(
                WBTempAuthoToken.new(), "cache/wb_temp_auth_token.txt", 30
            ).value(),
        )
        
        wb_goods_ids = goods_query.print(1, 1).products

        for id in wb_goods_ids:
            products.append(FakeProduct.new(id))

    page = MstacheHtmlPage.new("index.html")

    for product in products:
        data = product.print()

        page = page.with_data(
            "product",
            {
                "articul": data.articul,
                "name": data.name,
                "price": data.price,
                "image": data.images[0],
                "seller": data.seller_name,
                "quantity": data.quantity,
                "raiting": data.raiting,
                "reviews": data.reviews_count,
            },
        )

    return page.display()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
