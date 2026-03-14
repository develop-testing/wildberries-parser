from __future__ import annotations
from dataclasses import dataclass, asdict


from .products import Products
from .products import ProductData
from .products import ProductPrint


@dataclass(slots=True, frozen=True)
class Product(Products):
    number: int
    name: str
    data: ProductData

    def __post_init__(self):      
        if int(self.number) > 99999999999:
            raise ValueError('product id is too long')
        
        if self.data:
            for key, value in asdict(self.data).items():
                if len(str(key)) > 256:
                    raise ValueError('key exceeds 256 characters')
                if len(str(value)) > 256:
                    raise ValueError('value exceeds 256 characters')


    def print(self) -> ProductPrint:
        return ProductPrint(
            articul=self.number,
            name=self.name,
            descr="",
            images="",
            characters="",
            raiting="",
            reviews_count="",
            link="",
            price="",
            seller_name="",
            seller_link="",
            sizes="",
            quantity="",
        )