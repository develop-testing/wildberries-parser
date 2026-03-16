from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from goods.wildberries_goods import WildberriesGoods
from goods.fk_goods import FakeGoods
from goods.console_log_goods import ConsoleLogGoods
from goods.json_chached_goods import JsonFileCachedGoods

from product.fk_product import FakeProduct
from product.products import ProductData
from product.wildberries_product import WildberriesProduct
from product.json_cached_product import JsonCachedProduct
from product.console_log_product import ConsoleLogProduct

from data_table.pandas_data_table import PandasDataTable
from data_table.data_tables import DataTableRow
from data_table.console_log_data_table import ConsoleLogDataTable


@dataclass(frozen=True, slots=True)
class WildberriesApp:
    main_table_path: str
    second_table_path: str
    x_wbaas_token: str

    def __post_init__(self) -> None:
        if len(self.main_table_path) > 256:
            raise ValueError("main table name is too long")

        if len(self.second_table_path) > 256:
            raise ValueError("second table name is too long")

        if len(self.x_wbaas_token) > 600:
            raise ValueError("second table name is too long")

    def scrab_of(self, query: str) -> None:
        goods = ConsoleLogGoods(
            JsonFileCachedGoods.new(
                WildberriesGoods.new(query, self.x_wbaas_token), "cache/goods.json"
            )
        )

        printout = goods.print()

        main_products = []

        second_products = []

        def fetch_product(product_id: int) -> ProductData:
            try:
                return ConsoleLogProduct(
                    JsonCachedProduct(
                        WildberriesProduct.new(product_id, self.x_wbaas_token),
                        f"cache/products/product_{product_id}.json",
                    )
                ).print()
            except Exception as e:
                return ProductData.empty()

        pack_size = 100

        for i in range(0, len(printout.products), pack_size):
            pack = printout.products[i : i + pack_size]

            with ThreadPoolExecutor(max_workers=pack_size) as executor:
                result = list(executor.map(fetch_product, pack))
                result = [item for item in result if item]

                for product_print in result:
                    price = product_print.price or 0
                    raiting = product_print.raiting or 0

                    if (float(raiting) < 4.5 and int(price) < 10000):
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
                    f"{item.get('name', 'Неизвестно')}: {item.get('value', '-')}" 
                    for item in printout.characters
                ),
                seller_name=printout.seller_name,
                seller_link=printout.seller_link,
                sizes=", ".join(printout.sizes),
                quantity=str(printout.quantity),
                raiting=str(printout.raiting),
                reviews=str(printout.reviews_count),
            )

        ConsoleLogDataTable(PandasDataTable.new(self.main_table_path)).update(
            [map_printout_to_datarow(printout) for printout in main_products]
        )

        ConsoleLogDataTable(PandasDataTable.new(self.second_table_path)).update(
            [map_printout_to_datarow(printout) for printout in second_products]
        )


WildberriesApp(
    "result/all_product.xlsx",
    "result/filtered_product.xlsx",
    "1.1000.3c0234109f2f4703b35e7303f1c59d5a.MTV8OTUuMjYuNjQuMjI5fE1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NDsgcnY6MTQwLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvMTQwLjB8MTc3NDYwNzU0MHxyZXVzYWJsZXwyfGV5Sm9ZWE5vSWpvaUluMD18MHwzfDE3NzQwMDI3NDB8MQ==.MEQCIHbC2hNqZY7t0TB3PIRdJ9DUJAcCfL5S7hnyMmFToN9dAiA51lbY7zSowsJJqAz8UZFqWDbdHsNgYWcZ2uY1vQ6v3A==",
).scrab_of("пальто из натуральной шерсти")
