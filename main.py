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

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, query = "", marketplace = []):
    if marketplace == "wildberries":
        goods_query = WildberriesGoods.new(
            query,
            '1.1000.3c0234109f2f4703b35e7303f1c59d5a.MTV8OTUuMjYuNjQuMjI5fE1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NDsgcnY6MTQwLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvMTQwLjB8MTc3NDYwNzU0MHxyZXVzYWJsZXwyfGV5Sm9ZWE5vSWpvaUluMD18MHwzfDE3NzQwMDI3NDB8MQ==.MEQCIHbC2hNqZY7t0TB3PIRdJ9DUJAcCfL5S7hnyMmFToN9dAiA51lbY7zSowsJJqAz8UZFqWDbdHsNgYWcZ2uY1vQ6v3A=='
        )

    view_products = products = []

    wb_goods_ids = goods_query.print(1,1).products

    for id in wb_goods_ids:
        view_products.append(FakeProduct.new(id))

    page = MstacheHtmlPage.new('index.html')

    for product in products:
        data = product.print()

        page = page.with_data('product', {
            "articul": data.articul,
            "name": data.name,
            "price": data.price,
            "image": data.images[0],
            "seller": data.seller_name,
            "quantity": data.quantity,
            "raiting": data.raiting,
            "reviews": data.reviews_count,
        })

    return page.display()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
