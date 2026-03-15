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

from data_table.pandas_data_table import PandasDataTable
from data_table.data_tables import DataTableRow

goods = JsonFileCachedGoods.new(
    WildberriesScrappedGoods.new("пальто из натуральной шерсти"), "cache/goods.json"
)


printout = goods.print()


products_to_update = []

products_to_update.append(
    JsonCachedProduct(
        WildberriesProduct
            .new(204971561, '1.1000.3c0234109f2f4703b35e7303f1c59d5a.MTV8OTUuMjYuNjQuMjI5fE1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NDsgcnY6MTQwLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvMTQwLjB8MTc3NDYwNzU0MHxyZXVzYWJsZXwyfGV5Sm9ZWE5vSWpvaUluMD18MHwzfDE3NzQwMDI3NDB8MQ==.MEQCIHbC2hNqZY7t0TB3PIRdJ9DUJAcCfL5S7hnyMmFToN9dAiA51lbY7zSowsJJqAz8UZFqWDbdHsNgYWcZ2uY1vQ6v3A=='),
        f"cache/products/product_{204971561}.json"
    ).print()
)

print(products_to_update)

"""
for id in printout.products:
    products_to_update.append(
        JsonCachedProduct(
            WildberriesProduct
            .new(id), f"cache/products/product_{id}.json"
        ).print()
    )
"""
    
table = PandasDataTable.new("result/all_product.xlsx").update(
    [
        DataTableRow(
            product_link=printout.link,
            articul=printout.articul,
            name=printout.name,
            price=printout.price,
            descr=printout.descr,
            images=", ".join(printout.images),
            characters=", ".join(
                f"{item['name']}: {item['value']}" for item in printout.characters
            ),
            seller_name=printout.seller_name,
            seller_link=printout.seller_link,
            sizes=", ".join(printout.sizes),
            quantity=str(printout.quantity),
            raiting=str(printout.raiting),
            reviews=str(printout.reviews_count),
        )
        for printout in products_to_update
    ]
)
