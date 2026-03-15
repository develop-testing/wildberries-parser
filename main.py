from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from goods.scrapped_goods import WildberriesScrappedGoods
from goods.fk_goods import FakeGoods
from goods.json_chached_goods import JsonFileCachedGoods

from product.fk_product import FakeProduct
from product.wildberries_product import WildberriesProduct
from product.json_cached_product import JsonCachedProduct

goods = JsonFileCachedGoods.new(
    WildberriesScrappedGoods.new("пальто из натуральной шерсти"),
    "cache/goods.json"
)

printout = goods.print()

for id in [6489086, 11275582, 481144243]:
    # print(WildberriesProduct.new(id).print())
    print(
        JsonCachedProduct(
            FakeProduct.new(id),
            f"cache/products/product_{id}.json"
        )
        .print()
    )