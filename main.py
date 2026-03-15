from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from goods.wildberries_goods import WildberriesGoods
from goods.fk_goods import FakeGoods
from goods.json_chached_goods import JsonFileCachedGoods

from product.fk_product import FakeProduct
from product.products import ProductData
from product.wildberries_product import WildberriesProduct
from product.json_cached_product import JsonCachedProduct

from data_table.pandas_data_table import PandasDataTable
from data_table.data_tables import DataTableRow


@dataclass(frozen=True, slots=True)
class WildberriesCatalog:
    main_table_path: str
    second_table_path: str

    def __post_init__(self) -> None:
        if len(self.main_table_path) > 256:
            raise ValueError("main table name is too long")

        if len(self.second_table_path) > 256:
            raise ValueError("second table name is too long")

    def scrab_of(self, query: str) -> None:
        goods = JsonFileCachedGoods.new(WildberriesGoods.new(query), "cache/goods.json")

        printout = goods.print()

        main_products = []

        second_products = []

        def fetch_product(product_id: int) -> ProductData:
            try:
                return JsonCachedProduct(
                    FakeProduct.new(product_id),
                    f"cache/products/product_{product_id}.json",
                ).print()
            except Exception as e:
                return ProductData.empty()

        pack_size = 40

        for i in range(0, len(printout.products), pack_size):
            pack = printout.products[i : i + pack_size]

            with ThreadPoolExecutor(max_workers=pack_size) as executor:
                result = list(executor.map(fetch_product, pack))
                result = [item for item in result if item]

                for product_print in result:
                    if (
                        float(product_print.raiting) < 4.5
                        and int(product_print.price) < 10000
                    ):
                        second_products.append(product_print)

                main_products.extend(result)

        def map_printout_to_datarow(printout: ProductData) -> DataTableRow:
            return DataTableRow(
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

        PandasDataTable.new("result/all_product.xlsx").update(
            [map_printout_to_datarow(printout) for printout in main_products]
        )

        PandasDataTable.new("result/filtered_product.xlsx").update(
            [map_printout_to_datarow(printout) for printout in second_products]
        )


WildberriesCatalog("result/all_product.xlsx", "result/filtered_product.xlsx").scrab_of(
    "пальто из натуральной шерсти"
)
