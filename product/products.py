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
    characters: list[dict[str, str]]
    raiting: int
    reviews_count: int
    link: str
    price: str
    seller_name: str
    seller_link: str
    sizes: list[str]
    quantity: int
    source: str

    @staticmethod
    def empty() -> ProductData:
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
            quantity=0,
            source=""
        )


class Products(Protocol):
    def print(self) -> ProductData:
        pass
