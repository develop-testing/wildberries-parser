from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass, asdict


@dataclass(slots=True)
class ProductData:
    descr: str
    images: list[str]
    characters: list[str]
    raiting: int
    reviews_count: int
    link: str
    price: str
    seller_name: str
    seller_link: str
    sizes: list[str]
    quantity: int

    @staticmethod
    def empty() -> ProductData:
        return ProductData(
            descr="",
            images="",
            characters="",
            raiting="",
            reviews_count="",
            link="",
            price="",
            seller_name="",
            seller_link="",
            sizes="",
            quantity="",
        )


@dataclass(slots=True)
class ProductPrint(ProductData):
    articul: str
    name: str


class Products(Protocol):
    def print(self) -> ProductPrint:
        pass