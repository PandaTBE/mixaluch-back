import json
from typing import List
from django.http import HttpResponse
from config import EVOTOR_TOKEN
import requests
from store import models, serializers


def change_price_by_evotor(products: List[models.Product]):
    """Функция для изменения цен на сайте, используя данные эвотора

    Args:
        products (List[models.Product]): Все товары

    """
    BASE_EVOTOR_URL = "https://api.evotor.ru/api/v1/inventories/stores"
    HEADERS = {"X-Authorization": EVOTOR_TOKEN}
    EVOTOR_SOURCE = "evotor"

    # Получение всех магазинов (нужно, чтобы получить товары из разных отделов)
    all_stores_response = requests.get(f"{BASE_EVOTOR_URL}/search", headers=HEADERS)

    if all_stores_response.ok:
        stores_by_id = {}
        for store in all_stores_response.json():
            store_uuid = store["uuid"]
            stores_by_id[store_uuid] = {}

            # Ищем товары в каждом из отделов
            all_products_in_store_response = requests.get(
                f"{BASE_EVOTOR_URL}/{store_uuid}/products", headers=HEADERS
            )
            if all_products_in_store_response.ok:
                products_by_id = {}
                for product in all_products_in_store_response.json():
                    product_id = product["uuid"]
                    products_by_id[product_id] = product

                stores_by_id[store_uuid] = products_by_id

        if len(stores_by_id.keys()):
            # Итерация во всем товарам и поиск тех, у которых есть ссылка на товар эвотора
            for product in products:
                serialized_product = serializers.ProductSerializer(product).data
                external_id = next(
                    (
                        external_id
                        for external_id in serialized_product["external_ids"]
                        if external_id["data_source"] == EVOTOR_SOURCE
                    ),
                    None,
                )

                if external_id is not None:
                    splitted_id = external_id["external_id"].split("/")
                    store_uuid = splitted_id[0]
                    product_uuid = splitted_id[1]

                    # Получение товара эвотора
                    evotor_product = stores_by_id.get(store_uuid, {}).get(
                        product_uuid, None
                    )

                    # Если товар найден, то происходит обновление цен
                    if evotor_product is not None:
                        evotor_price = evotor_product.get("price", None)
                        if evotor_price is not None:
                            product.regular_price = evotor_price
                            product.discount_price = evotor_price
                            product.save()

            return HttpResponse("Цены обновлены!")

    return HttpResponse(f"Не удалось получить информацию от Эвотор.")
