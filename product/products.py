from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass, asdict


from dataclasses import dataclass, field
from typing import ClassVar

@dataclass(slots=True)
class ProductData:
    articul: str
    name: str
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
    def empty():
        return ProductData(
            articul="",
            name="",
            descr="",
            images=[],
            characters=[],
            raiting=0,
            reviews_count=0,
            link="",
            price="",
            seller_name="",
            seller_link="",
            sizes=[],
            quantity=0
        )


class Products(Protocol):
    def with_data(self, key: str, value: str) -> Products:
        pass

    def print(self) -> ProductData:
        pass