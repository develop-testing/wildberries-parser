from __future__ import annotations
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dataclasses import dataclass
from html_page.mstache_html_page import MstacheHtmlPage
from product.fk_product import FakeProduct


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    products = [
        FakeProduct.new(1),
        FakeProduct.new(2),
        FakeProduct.new(3),
        FakeProduct.new(4),
    ]

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
