from __future__ import annotations
import os
from dataclasses import dataclass
from datetime import datetime, timedelta


from .temp_auth_tokens import TempAuthoTokens


@dataclass(slots=True)
class CachedTempAuthoToken(TempAuthoTokens):
    origin: TempAuthoTokens
    file_path: str
    expired_seconds: int

    def _fetch_and_save(self) -> str:
        value = self.origin.value()

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(value)

        return value

    def value(self) -> str:
        if not os.path.exists(self.file_path):
            return self._fetch_and_save()

        file_mtime = os.path.getmtime(self.file_path)
        file_time = datetime.fromtimestamp(file_mtime)
        current_time = datetime.now()

        if current_time - file_time > timedelta(seconds=self.expired_seconds):
            return self._fetch_and_save()

        with open(self.file_path, "r", encoding="utf-8") as f:
            value = f.read().strip()

        return value

    def new(
        origin: TempAuthoTokens, file_path: str, expired_seconds: int
    ) -> CachedTempAuthoToken:
        return CachedTempAuthoToken(origin, file_path, expired_seconds)