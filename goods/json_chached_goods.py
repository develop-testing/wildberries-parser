from __future__ import annotations
from dataclasses import dataclass
import os
import json


from .goods import Goods
from .goods import GoodsPrint


@dataclass(slots=True, frozen=True)
class JsonFileCachedGoods(Goods):
    origin: Goods
    file_path: str

    def query(self) -> str:
        return self.origin.query()

    def print(self) -> GoodsPrint:
        if (not os.path.exists(self.file_path)) or os.path.getsize(self.file_path) == 0:
            printout = self.origin.print()

            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(printout.products, f, ensure_ascii=False)
            
            return printout

        with open(self.file_path, "r", encoding="utf-8") as f:
            products = json.load(f)

        return GoodsPrint(
            query=self.origin.query(),
            count=len(products),
            products=products
        )
    
    @staticmethod
    def new(origin: Goods, file_path: str) -> JsonFileCachedGoods:
        return JsonFileCachedGoods(origin, file_path)