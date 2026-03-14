from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass


@dataclass(slots=True)
class GoodsPrint:
    query: str
    count: int
    products: str


class Goods(Protocol):
    def print(self) -> GoodsPrint:
        pass
