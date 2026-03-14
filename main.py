from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass, asdict

from goods.scrapped_goods import WildberriesScrappedGoods
from goods.fk_goods import FakeGoods
from goods.json_chached_goods import JsonFileCachedGoods

@dataclass(slots=True)
class ProductData:
    descr: str
    images: list[str]
    characters: list[str]
    raiting: int
    reviews_count: int
    link: str
    price: str
    seller_name: str
    seller_link: str
    sizes: list[str]
    quantity: int

    @staticmethod
    def empty() -> ProductData:
        return ProductData(
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

@dataclass(slots=True)
class ProductPrint(ProductData):
    articul: str
    name: str

@dataclass(slots=True, frozen=True)
class Product:
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

goods = JsonFileCachedGoods.new(
    WildberriesScrappedGoods.new("пальто из натуральной шерсти"),
    "cache/goods.json"
)

printout = goods.print()

for id in printout.products:
    print(
        Product(id, "", ProductData.empty())
        .print()
    )