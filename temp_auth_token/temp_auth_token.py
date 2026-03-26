from __future__ import annotations
from dataclasses import dataclass

from .temp_auth_tokens import TempAuthoTokens

@dataclass(frozen=True, slots=True)
class TempAuthoToken(TempAuthoTokens):
    content: str

    def __post_init__(self) -> None:
        if len(self.content) > 1024 or len(self.content) < 50:
            raise ValueError("incorect size of temp auth token")

    def value(self) -> str:
        return self.content