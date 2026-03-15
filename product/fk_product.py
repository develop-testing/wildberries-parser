from __future__ import annotations
from dataclasses import dataclass
import random
from time import sleep


from .products import Products
from .products import ProductData
from .product import Product


@dataclass(slots=True, frozen=True)
class FakeProduct(Products):
    origin: Products

    def print(self) -> ProductData:
        data = self.origin.print()

        data.articul = str(random.randint(100000, 999999))
        data.name = "Фейковый товар " + str(random.randint(1, 100))
        data.descr = "Описание фейкового товара для тестирования"
        data.images = ["fake_img1.jpg", "fake_img2.jpg"]
        data.characters = [
            {"name": f"тест-{i}", "value": f"тест-{i}"} for i in range(0, 20)
        ]
        data.raiting = random.randint(1, 5)
        data.reviews_count = random.randint(0, 1000)
        data.link = "https://fake-shop.ru/product/" + str(random.randint(1000, 9999))
        data.price = str(random.randint(500, 10000))
        data.seller_name = "Фейковый продавец"
        data.seller_link = "https://fake-shop.ru/seller/" + str(random.randint(1, 100))
        data.sizes = ["S", "M", "L", "XL"]
        data.quantity = random.randint(0, 50)

        return data

    @staticmethod
    def new(id: int) -> FakeProduct:
        return FakeProduct(Product(id, ProductData.empty()))
