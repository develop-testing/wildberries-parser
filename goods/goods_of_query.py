from __future__ import annotations
from dataclasses import dataclass


from .goods import Goods
from .goods import GoodsPrint


@dataclass(slots=True, frozen=True)
class GoodsOfhQuery(Goods):
    query: str
    products: list[int]

    def __post_init__(self):
        if len(self.query) > 500:
            raise ValueError("query of goods is too long")
        
        if not isinstance(self.query, str):
            raise ValueError("query of goods is not string")
        
        if self.products:
            for value in self.products:
                if not isinstance(value, int):
                    raise ValueError("product id is not int")

                if value > 99999999999:
                    raise ValueError("product id is too long")


    def print(self) -> GoodsPrint:
        printout = GoodsPrint(
            query=self.query,
            count=len(self.products),
            products=self.products
        )

        return printout