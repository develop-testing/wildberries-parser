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

for id in printout.products:
    products_to_update.append(
        JsonCachedProduct(
            FakeProduct.new(id), f"cache/products/product_{id}.json"
        ).print()
    )

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
