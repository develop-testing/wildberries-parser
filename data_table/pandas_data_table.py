from __future__ import annotations
from dataclasses import dataclass, asdict
import pandas as pd
import os


from .data_tables import  DataTables
from .data_tables import DataTableRow
from .data_table import DataTable


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