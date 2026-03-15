from __future__ import annotations
from dataclasses import dataclass
import time

from .data_tables import DataTables
from .data_tables import DataTableRow


@dataclass(slots=True, frozen=True)
class ConsoleLogDataTable(DataTables):
    origin: DataTables

    def update(self, rows: list[DataTableRow]) -> DataTables:
        start = time.perf_counter()

        print("start of data table update")
        new_table = self.origin.update(rows)
        print(f"finish of data table update (time: {time.perf_counter() - start:.4f}s)")

        return ConsoleLogDataTable(new_table)

    def print(self) -> list[DataTableRow]:
        start = time.perf_counter()
        print("start of data table print")
        data = self.origin.print()
        print(f"finish of data table print (time: {time.perf_counter() - start:.4f}s)")
        return data

    @staticmethod
    def new(origin: DataTables) -> ConsoleLogDataTable:
        start = time.perf_counter()
        table = ConsoleLogDataTable(origin)
        print(f"data table is created (time: {time.perf_counter() - start:.4f}s)")
        return table
