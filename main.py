from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass

from goods.scrapped_goods import WildberriesScrappedGoods
from goods.fk_goods import FakeGoods
from goods.json_chached_goods import JsonFileCachedGoods

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

print(
    JsonFileCachedGoods.new(
        WildberriesScrappedGoods.new("пальто из натуральной шерсти"),
        "cache/goods.json"
    ).print().count
)

"""
print(
    JsonFileCachedGoods.new(
        WildberriesScrappedGoods.new("пальто из натуральной шерсти"),
        "cache/goods.json"
    ).print()
)
"""

"""
print(
    JsonFileCachedGoods.new(
        FakeGoods.new("пальто из натуральной шерсти", 9999),
        "cache/goods.json"
    ).print()
)"""