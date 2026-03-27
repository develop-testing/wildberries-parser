from __future__ import annotations
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dataclasses import dataclass
from html_page.mstache_html_page import MstacheHtmlPage
from product.fk_product import FakeProduct
from product.wildberries_product import WildberriesProduct
from goods.wildberries_goods import WildberriesGoods
from temp_auth_token.wb_temp_auth_token import WBTempAuthoToken
from temp_auth_token.cached_temp_auth_token import CachedTempAuthoToken

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> str:
    marketplace = request.query_params.getlist("marketplace")
    query = request.query_params.get("query", "")
    page = request.query_params.get("page", "")
    limit = 10

    temp_token = CachedTempAuthoToken.new(
        WBTempAuthoToken.new(),
        "cache/wb_temp_auth_token.txt",
        86400
    )

    products: list[FakeProduct] = []

    if "wildberries" in marketplace:
        goods_query = WildberriesGoods.new(
            query,
            temp_token.value()
        )

        wb_goods_ids = goods_query.fetch(120, 10).products

        for id in wb_goods_ids:
            products.append(
                WildberriesProduct.new(id, temp_token.value())
            )

    page = MstacheHtmlPage.new("index.html")

    for product in products:
        data = product.print()
        
        page = page.with_data(
            "product",
            {
                "link": data.link,
                "articul": data.articul,
                "name": data.name,
                "price": data.price,
                "image": data.images[0] if data.images else "",
                "seller": data.seller_name,
                "quantity": data.quantity,
                "raiting": data.raiting,
                "reviews": data.reviews_count,
            },
        )

    return page.display()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
