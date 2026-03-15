from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass


@dataclass(slots=True)
class GoodsPrint:
    query: str
    count: int
    products: list[int]


class Goods(Protocol):
    def query(self) -> str:
        pass

    def print(self) -> GoodsPrint:
        pass
