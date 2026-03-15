from __future__ import annotations
from dataclasses import dataclass, asdict
import os
import json


from .products import Products
from .products import ProductData
from .product import Product


@dataclass(slots=True, frozen=True)
class JsonCachedProduct(Products):
    origin: Products
    file_path: str

    def print(self) -> ProductData:
        directory = os.path.dirname(self.file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.file_path):
            printout = self.origin.print()

            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(asdict(printout), f, ensure_ascii=False, indent=4)
            
            return printout

        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

        return ProductData(
            articul=data["articul"],
            name=data["name"],
            descr=data["escr"],
            images=data["images"],
            characters=data["characters"],
            raiting=data["raiting"],
            reviews_count=data["reviews_count"],
            link=data["link"],
            price=data["price"],
            seller_name=data["seller_name"],
            seller_link=data["seller_link"],
            sizes=data["sizes"],
            quantity=data["quantity"],
        )
    
    @staticmethod
    def new(origin: Products, file_path: str) -> JsonCachedProduct:
        return JsonCachedProduct(origin, file_path)