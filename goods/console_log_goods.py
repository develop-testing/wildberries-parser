from __future__ import annotations
from dataclasses import dataclass
import time


from .goods import Goods
from .goods import GoodsPrint


@dataclass(slots=True, frozen=True)
class ConsoleLogGoods(Goods):
    origin: Goods

    def query(self) -> str:
        start = time.perf_counter()
        print("start of get goods query")
        data = self.origin.query()
        print(f"finish of get goods query (time: {time.perf_counter() - start:.2f}s)")
        return data

    def print(self, page_start: int, page_end: int) -> GoodsPrint:
        start = time.perf_counter()
        print("start of goods print")
        data = self.origin.print(page_start, page_end)
        print(f"finish of goods print (time: {time.perf_counter() - start:.2f}s)")
        return data

    @staticmethod
    def new(origin: Goods) -> "ConsoleLogGoods":
        start = time.perf_counter()
        goods = ConsoleLogGoods(origin)
        print(f"goods is created (time: {time.perf_counter() - start:.4f}s)")
        return goods
