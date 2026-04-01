from __future__ import annotations
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dataclasses import dataclass
from html_page.mstache_html_page import MstacheHtmlPage
from product.fk_product import FakeProduct
from product.wildberries_product import WildberriesProduct
from product.console_log_product import ConsoleLogProduct
from goods.wildberries_goods import WildberriesGoods
from temp_auth_token.wb_temp_auth_token import WBTempAuthoToken
from temp_auth_token.cached_temp_auth_token import CachedTempAuthoToken


from concurrent.futures import ThreadPoolExecutor, as_completed


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> str:
    query = request.query_params.get("query", "")
    
    if not query:
        html_page = MstacheHtmlPage.new("index.html")
        html_page = html_page.with_data("query", "")
        return html_page.display()
    
    page = int(request.query_params.get("page", 0))
    limit = 8

    temp_token = CachedTempAuthoToken.new(
        WBTempAuthoToken.new(),
        "cache/wb_temp_auth_token.txt",
        86400
    )

    products: list[FakeProduct] = []

    goods_query = WildberriesGoods.new(
        query,
        temp_token.value()
    )

    wb_goods_ids = goods_query.fetch(page * limit, limit).products

    for id in wb_goods_ids:
        products.append(
            ConsoleLogProduct.new(
                WildberriesProduct.new(id, temp_token.value())
            )
        )

    html_page = MstacheHtmlPage.new("index.html")

    def process_product(product):
        data = product.print()
        return {
            "link": data.link,
            "articul": data.articul,
            "name": data.name,
            "price": data.price,
            "image": data.images[0] if data.images else "",
            "seller": data.seller_name,
            "quantity": data.quantity,
            "raiting": data.raiting,
            "reviews": data.reviews_count,
            "source": data.source
        }

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_product, product) for product in products]
        
        for future in as_completed(futures):
            product_data = future.result()
            html_page = html_page.with_data("product", product_data)
    
    def build_url(page, query):
        return f"/?page={page}&query={query}"

    html_page = (
        html_page
            .with_data(
                "prev_url",
                build_url(page - 1, query) if page > 1 else None
            )
            .with_data(
                "next_url",
                build_url(page + 1, query)
            )
            .with_data("query", query)
    )

    return html_page.display()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)