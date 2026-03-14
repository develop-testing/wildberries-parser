from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from goods.scrapped_goods import WildberriesScrappedGoods
from goods.fk_goods import FakeGoods
from goods.json_chached_goods import JsonFileCachedGoods

from product.fk_product import FakeProduct
from product.wildberries_product import WildberriesProduct

goods = JsonFileCachedGoods.new(
    WildberriesScrappedGoods.new("пальто из натуральной шерсти"),
    "cache/goods.json"
)

printout = goods.print()

import time
start = time.time()

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(WildberriesProduct.new(id).print)
        for id in [6489086, 11275582, 481144243]
    ]

    for future in as_completed(futures):
        result = future.result()
        print(result)

print(f"Общее время: {time.time() - start:.2f} сек")
