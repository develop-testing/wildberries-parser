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

    def print(self) -> list[DataTableRow]:
        pass


@dataclass(slots=True, frozen=True)
class DataTable(DataTables):
    rows: list[DataTableRow]
    
    def update(self, rows: list[DataTableRow]) -> DataTable:
        return DataTable(self.rows + rows)
    
    def print(self) -> list[DataTableRow]:
        return self.rows


import pandas as pd
import os

@dataclass(slots=True)
class PandasDataTable(DataTables):
    origin: DataTables
    file_path: str

    def update(self, rows: list[DataTableRow]) -> PandasDataTable:
        if os.path.exists(self.file_path):
            existing_df = pd.read_excel(self.file_path)
            data_list = existing_df.to_dict(orient='records')

            stored_data = [
                DataTableRow(
                    product_link=row["product_link"],
                    articul=row["articul"],
                    name=row["name"],
                    price=row["price"],
                    descr=row["descr"],
                    images=row["images"],
                    characters=row["characters"],
                    seller_name=row["seller_name"],
                    seller_link=row["seller_link"],
                    sizes=row["sizes"],
                    quantity=row["quantity"],
                    raiting=row["raiting"],
                    reviews=row["reviews"],
                )
                for row in data_list
            ]

            rows = rows + stored_data

        new_origin = self.origin.update(rows)

        df = pd.DataFrame([asdict(row) for row in rows])
        df.to_excel(self.file_path, index=False)

        return PandasDataTable(new_origin, self.file_path)
    
    def print(self) -> list[DataTableRow]:
        data = self.origin.print()

        if not data:
            if os.path.exists(self.file_path):
                existing_df = pd.read_excel(self.file_path)
                data_list = existing_df.to_dict(orient='records')

                data = [
                    DataTableRow(
                        product_link=row["product_link"],
                        articul=row["articul"],
                        name=row["name"],
                        price=row["price"],
                        descr=row["descr"],
                        images=row["images"],
                        characters=row["characters"],
                        seller_name=row["seller_name"],
                        seller_link=row["seller_link"],
                        sizes=row["sizes"],
                        quantity=row["quantity"],
                        raiting=row["raiting"],
                        reviews=row["reviews"],
                    )
                    for row in data_list
                ]

                self.origin = self.origin.update(data)
        

        return data
    
    @staticmethod
    def new(file_path: str) -> PandasDataTable:
        return PandasDataTable(DataTable([]), file_path)


products_to_update = []

for id in printout.products:
    products_to_update.append(
        JsonCachedProduct(
            FakeProduct.new(id),
            f"cache/products/product_{id}.json"
        )
        .print()
    )

table = PandasDataTable\
    .new("result/all_product.xlsx")\
    .update([
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
