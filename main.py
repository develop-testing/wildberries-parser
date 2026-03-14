from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass

from goods.scrapped_goods import WildberriesScrappedGoods

@dataclass(slots=True)
class ProductPrint:
    descr: str
    images: list[str]
    characters: list[str]
    raiting: int
    reviews_count: int
    link: str
    articul: str
    name: str
    price: str
    seller_name: str
    seller_link: str
    sizes: list[str]
    quantity: int


WildberriesScrappedGoods\
    .new("пальто из натуральной шерсти")\
    .then(lambda goods: goods.print())\
    .then(print)\
    .catch(print)