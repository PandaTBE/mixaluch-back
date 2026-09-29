from types import SimpleNamespace
from unittest.mock import patch
from uuid import UUID

import requests
from django.core.cache import cache
from django.test import SimpleTestCase
from django.urls import Resolver404, resolve
from rest_framework.test import APIRequestFactory, force_authenticate

from store.evotor_views import EvotorProductsView, EvotorStoresView


class EvotorViewsTests(SimpleTestCase):
    def setUp(self):
        cache.clear()

    def request(self, view, staff=True, **kwargs):
        request = APIRequestFactory().get("/api/admin/evotor/stores/")
        if staff is not None:
            force_authenticate(request, user=SimpleNamespace(is_staff=staff, is_authenticated=True, pk=1))
        return view.as_view()(request, **kwargs)

    @patch("store.evotor_views.requests.get")
    def test_non_staff_cannot_call_upstream(self, get):
        for staff in (None, False):
            self.assertIn(self.request(EvotorStoresView, staff).status_code, (401, 403))
        get.assert_not_called()

    @patch("store.evotor_views.EVOTOR_TOKEN", "test-server-secret")
    @patch("store.evotor_views.requests.get")
    def test_staff_proxy_uses_server_token_and_fixed_url(self, get):
        get.return_value.json.return_value = [{"uuid": "example"}]
        response = self.request(EvotorStoresView)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"uuid": "example"}])
        get.assert_called_once_with(
            "https://api.evotor.ru/api/v1/inventories/stores/search",
            headers={"X-Authorization": "test-server-secret"}, timeout=(5, 20), allow_redirects=False,
        )
        store_id = UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
        self.assertEqual(self.request(EvotorProductsView, store_id=store_id).status_code, 200)
        self.assertTrue(get.call_args.args[0].endswith(f"/{store_id}/products"))

    @patch("store.evotor_views.EVOTOR_TOKEN", "test-server-secret")
    @patch("store.evotor_views.requests.get")
    def test_upstream_errors_and_invalid_payload_are_sanitized(self, get):
        for error in (requests.Timeout("sensitive"), requests.HTTPError("sensitive"), ValueError("sensitive")):
            get.side_effect = error
            response = self.request(EvotorStoresView)
            self.assertEqual(response.status_code, 502)
            self.assertNotIn("sensitive", str(response.data))
        get.side_effect = None
        get.return_value.json.return_value = {"unexpected": "payload"}
        self.assertEqual(self.request(EvotorStoresView).status_code, 502)

    @patch("store.evotor_views.EVOTOR_TOKEN", "")
    @patch("store.evotor_views.requests.get")
    def test_missing_configuration_does_not_call_upstream(self, get):
        self.assertEqual(self.request(EvotorStoresView).status_code, 503)
        get.assert_not_called()

    def test_malformed_store_id_is_rejected_by_route(self):
        with self.assertRaises(Resolver404):
            resolve("/api/admin/evotor/stores/not-a-uuid/products/")

    @patch("store.evotor_views.EVOTOR_TOKEN", "test-server-secret")
    @patch("store.evotor_views.requests.get")
    def test_uppercase_store_id_is_preserved(self, get):
        store_id = "20250130-E3FC-40C8-8000-8C087AC8E377"
        get.return_value.json.return_value = []
        match = resolve(f"/api/admin/evotor/stores/{store_id}/products/")
        self.assertEqual(self.request(EvotorProductsView, store_id=match.kwargs["store_id"]).status_code, 200)
        self.assertTrue(get.call_args.args[0].endswith(f"/{store_id}/products"))

    @patch("store.evotor_views.EVOTOR_TOKEN", "test-server-secret")
    @patch("store.evotor_views.requests.get")
    def test_staff_requests_are_rate_limited(self, get):
        get.return_value.json.return_value = []
        for _ in range(90):
            self.assertEqual(self.request(EvotorStoresView).status_code, 200)
        self.assertEqual(self.request(EvotorStoresView).status_code, 429)
        self.assertEqual(get.call_count, 90)
