from typing import Protocol


class TempAuthoTokens(Protocol):
    def value(self) -> str:
        pass