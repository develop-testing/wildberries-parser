from __future__ import annotations
from dataclasses import dataclass


from .goods import Goods
from .goods import GoodsPrint


@dataclass(slots=True, frozen=True)
class GoodsOfhQuery(Goods):
    query_string: str
    products: list[int]

    def __post_init__(self) -> None:
        if len(self.query_string) > 500:
            raise ValueError("query of goods is too long")

        if not isinstance(self.query_string, str):
            raise ValueError("query of goods is not string")

        if self.products:
            for value in self.products:
                if not isinstance(value, int):
                    raise ValueError("product id is not int")

                if value > 99999999999:
                    raise ValueError("product id is too long")

    def query(self) -> str:
        return self.query_string

    def fetch(self, from_number: int, count: int) -> GoodsPrint:
        if from_number > 999 or count > 999:
            raise ValueError("from_number or count is too long")
        
        if from_number < 0 or count < 0:
            raise ValueError("from_number or count is too small")
        
        if from_number >= len(self.products):
            return GoodsPrint(
                query=self.query(),
                count=0,
                products=[]
            )
        
        result = self.products[from_number:from_number + count]
        
        printout = GoodsPrint(
            query=self.query(),
            count=len(result),
            products=result
        )
        
        return printout
