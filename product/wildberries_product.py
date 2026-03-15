from __future__ import annotations
from dataclasses import dataclass
from DrissionPage import ChromiumPage, ChromiumOptions, SessionPage  # type: ignore
from time import sleep

from .products import Products
from .products import ProductData
from .product import Product


@dataclass(slots=True, frozen=True)
class WildberriesProduct(Products):
    origin: Products

    def print(self) -> ProductData:
        try:
            data = self.origin.print()

            articul_str = str(data.articul)
            vol_num = "0"
            part_num = "0"

            match len(articul_str):
                case 7:
                    vol_num = articul_str[:2]
                    part_num = articul_str[:4]
                case 8:
                    vol_num = articul_str[:3]
                    part_num = articul_str[:5]
                case 9:
                    vol_num = articul_str[:4]
                    part_num = articul_str[:6]

            options = ChromiumOptions()
            options.set_argument("--no-sandbox")
            options.set_argument("--disable-blink-features=AutomationControlled")
            options.set_user_agent(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            options.set_argument("--disable-notifications")
            options.set_argument("--disable-extensions")
            options.set_argument("--headless=new")
            web_page = ChromiumPage(addr_or_opts=options)

            url = f"https://mns-basket-cdn-02.geobasket.net/vol{vol_num}/part{part_num}/{articul_str}/info/ru/card.json"

            web_page.get(url)

            first_data = web_page.json

            web_page.get(
                f"https://www.wildberries.ru/__internal/u-card/cards/v4/detail?appType=1&curr=rub&dest=-1257786&spp=30&hide_vflags=4294967296&ab_testing=false&lang=ru&nm={articul_str}"
            )

            second_data = web_page.json

            max_images = 99
            image_counter = 1
            images = []

            session = SessionPage()

            while image_counter <= max_images:
                url = f"https://mns-basket-cdn-02.geobasket.net/vol{vol_num}/part{part_num}/{articul_str}/images/big/{image_counter}.webp"

                result = session.session.head(url)

                if result.status_code == 200:
                    images.append(url)
                    image_counter += 1
                    sleep(0.3)
                    continue

                break

            data.price = str(
                next(
                    (
                        s.get("price", {}).get("product", 0) // 100
                        for s in second_data["products"][0].get("sizes", [])
                        if s.get("price")
                    ),
                    0,
                )
            )
            data.name = first_data["imt_name"]
            data.descr = first_data["description"]
            data.images = images
            data.characters = first_data["options"]
            data.raiting = int(second_data["products"][0]["reviewRating"])
            data.reviews_count = int(second_data["products"][0]["nmFeedbacks"])
            data.link = f"https://www.wildberries.ru/catalog/{data.articul}/detail.aspx"
            data.seller_name = first_data["selling"]["brand_name"]
            data.seller_link = f"https://www.wildberries.ru/brands/{data.seller_name}"
            data.sizes = [size["name"] for size in second_data["products"][0]["sizes"]]
            data.quantity = int(second_data["products"][0]["totalQuantity"])

            return data

        except Exception as e:
            return data

        finally:
            web_page.quit()

    @staticmethod
    def new(id: int) -> WildberriesProduct:
        return WildberriesProduct(Product(id, ProductData.empty()))
