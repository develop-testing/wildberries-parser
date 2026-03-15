from __future__ import annotations
from dataclasses import dataclass


from .data_tables import DataTables
from .data_tables import DataTableRow


@dataclass(slots=True, frozen=True)
class DataTable(DataTables):
    rows: list[DataTableRow]

    def update(self, rows: list[DataTableRow]) -> DataTable:
        return DataTable(self.rows + rows)

    def print(self) -> list[DataTableRow]:
        return self.rows
