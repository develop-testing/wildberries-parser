from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass, asdict

from goods.scrapped_goods import WildberriesScrappedGoods
from goods.fk_goods import FakeGoods
from goods.json_chached_goods import JsonFileCachedGoods

from product.product import Product, ProductData

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