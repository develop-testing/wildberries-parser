from __future__ import annotations
from dataclasses import dataclass
from promise import Promise
import random


from .goods import Goods
from .goods import GoodsPrint
from .base_goods import GoodsOfhQuery


@dataclass(slots=True)
class FakeGoods(Goods):
    origin: Goods
    limit: int

    def query(self) -> str:
        return self.origin.query()

    def print(self, page_start: int, page_end: int) -> GoodsPrint:
        self.origin = GoodsOfhQuery(
            self.origin.query(),
            [random.randint(111111, 999999) for i in range(self.limit)],
        )

        return self.origin.print(page_start, page_end)

    @staticmethod
    def new(query: str, limit: int) -> FakeGoods:
        return FakeGoods(GoodsOfhQuery(query, []), limit)
