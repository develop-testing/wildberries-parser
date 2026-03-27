from __future__ import annotations
from dataclasses import dataclass
from DrissionPage import ChromiumPage, ChromiumOptions  # type: ignore[import-untyped]
from time import sleep

from .temp_auth_tokens import TempAuthoTokens
from .temp_auth_token import TempAuthoToken

@dataclass(slots=True)
class WBTempAuthoToken(TempAuthoTokens):
    origin: TempAuthoTokens | None

    def value(self) -> str:
        if not self.origin:
            co = ChromiumOptions()
            co.set_argument("--headless=new")  # New headless mode (better stealth)
            co.set_argument("--window-size=1920,1080")
            co.set_argument("--disable-blink-features=AutomationControlled")
            co.set_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

            # Disable automation flags
            co.set_argument("--disable-features=ChromeWhatsNewUI,IsolateOrigins,site-per-process")
            co.set_argument("--disable-web-security")
            co.set_argument("--disable-extensions")

            page = ChromiumPage(co)

            page.set.headers(
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "Cache-Control": "max-age=0",
                }
            )

            page.get("https://www.wildberries.ru/")
            page.wait.load_start()

            cookies = page.cookies()

            value = ""

            print(cookies)

            for cookie in cookies:
                if cookie["name"] == "x_wbaas_token":
                    value = cookie["value"]

            self.origin = TempAuthoToken(value)

            page.quit()

        return self.origin.value()

    @staticmethod
    def new() -> WBTempAuthoToken:
        return WBTempAuthoToken(None)