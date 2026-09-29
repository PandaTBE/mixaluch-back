import requests
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from config import EVOTOR_TOKEN


class EvotorThrottle(UserRateThrottle):
    rate = "90/min"


def evotor_response(path):
    if not EVOTOR_TOKEN:
        return Response({"detail": "Интеграция с Эвотор не настроена."}, status=503)
    try:
        response = requests.get(
            f"https://api.evotor.ru/api/v1/inventories/stores/{path}",
            headers={"X-Authorization": EVOTOR_TOKEN},
            timeout=(5, 20),
            allow_redirects=False,
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            raise ValueError("Unexpected Evotor response")
    except (requests.RequestException, ValueError):
        return Response({"detail": "Не удалось получить данные Эвотор. Попробуйте позже."}, status=502)
    return Response(data)


class EvotorStoresView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [EvotorThrottle]

    def get(self, request):
        return evotor_response("search")


class EvotorProductsView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [EvotorThrottle]

    def get(self, request, store_id):
        return evotor_response(f"{store_id}/products")
