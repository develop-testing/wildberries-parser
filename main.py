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

@dataclass(slots=True, frozen=True)
class DataTableRow:
    product_link: str
    articul: str
    name: str
    price: str
    descr: str
    images: list[str]
    characters: list[str]
    seller_name: str
    seller_link: str
    sizes: list[str]
    quantity: str
    raiting: str
    reviews: str

class DataTables(Protocol):
    def update(self, rows: list[DataTableRow]) -> DataTables:
        pass

@dataclass(slots=True, frozen=True)
class DataTable(DataTables):
    name: str
    rows: list

    def update(self, rows: list[DataTableRow]) -> DataTable:
        return DataTable(self.name, self.rows + rows)

table = DataTable("simple_products", [])

products_to_update = []

for id in [6489086, 11275582, 481144243]:
    products_to_update.append(
        JsonCachedProduct(
            WildberriesProduct.new(id),
            f"cache/products/product_{id}.json"
        )
        .print()
    )

table = table.update([
    DataTableRow(
        product_link=printout.link,
        articul=printout.articul,
        name=printout.name,
        price=printout.price,
        descr=printout.descr,
        images=", ".join(printout.images),
        characters=", ".join(f"{item['name']}: {item['value']}" for item in printout.characters),
        seller_name=printout.seller_name,
        seller_link=printout.seller_link,
        sizes=", ".join(printout.sizes),
        quantity=printout.quantity,
        raiting=printout.raiting,
        reviews=printout.reviews_count,
    )
    for printout in products_to_update
])
