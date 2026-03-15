from __future__ import annotations
from dataclasses import dataclass
import time


from .products import Products
from .products import ProductData


@dataclass(slots=True, frozen=True)
class ConsoleLogProduct(Products):
    origin: Products

    def print(self) -> ProductData:
        start = time.perf_counter()
        print("start of product print")
        data = self.origin.print()
        print(
            f"finish of product print {data.articul} (time: {time.perf_counter() - start:.2f}s)"
        )
        return data

    @staticmethod
    def new(origin: Products) -> ConsoleLogProduct:
        start = time.perf_counter()
        product = ConsoleLogProduct(origin)
        print(f"fake product is created (time: {time.perf_counter() - start:.4f}s)")
        return product
