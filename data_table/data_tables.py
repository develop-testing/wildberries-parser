from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DataTableRow:
    product_link: str
    articul: str
    name: str
    price: str
    descr: str
    images: list[str]
    characters: list[str]
    seller_name: str
    seller_link: str
    sizes: list[str]
    quantity: str
    raiting: str
    reviews: str


class DataTables(Protocol):
    def update(self, rows: list[DataTableRow]) -> DataTables:
        pass

    def print(self) -> list[DataTableRow]:
        pass
