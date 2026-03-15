from __future__ import annotations
from dataclasses import dataclass
from DrissionPage import ChromiumPage, ChromiumOptions, SessionPage, SessionOptions # type: ignore
from time import sleep

from .products import Products
from .products import ProductData
from .product import Product


@dataclass(slots=True, frozen=True)
class WildberriesProduct(Products):
    origin: Products
    x_wbaas_token: str

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

            page = SessionPage()

            page.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Referer': 'https://www.wildberries.ru',
                'Accept': '*/*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            })

            page.session.cookies.update({'x_wbaas_token': self.x_wbaas_token})

            page.get(f"https://mns-basket-cdn-02.geobasket.net/vol{vol_num}/part{part_num}/{articul_str}/info/ru/card.json")

            first_data = page.json

            page.get(f"https://www.wildberries.ru/__internal/u-card/cards/v4/detail?appType=1&curr=rub&dest=-1257786&spp=30&hide_vflags=4294967296&ab_testing=false&lang=ru&nm={articul_str}")

            second_data = page.json

            max_images = 99
            image_counter = 1
            images = []

            while image_counter <= max_images:
                url = f"https://mns-basket-cdn-02.geobasket.net/vol{vol_num}/part{part_num}/{articul_str}/images/big/{image_counter}.webp"

                result = page.session.head(url)

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
            data.seller_name = (first_data.get("selling") or {}).get("brand_name") or ""
            data.seller_link = f"https://www.wildberries.ru/brands/{data.seller_name}"
            data.sizes = [size["name"] for size in second_data["products"][0]["sizes"]]
            data.quantity = int(second_data["products"][0]["totalQuantity"])

            return data

        except Exception as e:
            return data

    @staticmethod
    def new(id: int, x_wbaas_token: str) -> WildberriesProduct:
        return WildberriesProduct(
            Product(id, ProductData.empty()),
            x_wbaas_token
        )
