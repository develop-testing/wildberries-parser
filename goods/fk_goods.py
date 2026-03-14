from __future__ import annotations
from dataclasses import dataclass
from promise import Promise
import random


from .goods import Goods
from .goods import GoodsPrint
from .goods_of_query import GoodsOfhQuery


@dataclass(slots=True, frozen=True)
class FakeGoods(Goods):
    origin: Goods

    def query(self) -> str:
        return self.origin.query()

    def print(self) -> GoodsPrint:
        return self.origin.print()
    
    @staticmethod
    def new(query: str) -> Promise[FakeGoods]:
        return GoodsOfhQuery(query, [
            random.randint(111111, 999999) for i in range(9999)
        ])