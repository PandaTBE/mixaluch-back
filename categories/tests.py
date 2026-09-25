from django.test import TestCase
from rest_framework.test import APIClient

from .models import Category


class CategoryVisibilityTests(TestCase):
    def test_list_exposes_visibility_without_hiding_admin_categories(self):
        active = Category.objects.create(name="Активная", slug="active")
        hidden = Category.objects.create(name="Скрытая", slug="hidden", is_active=False)
        response = APIClient().get("/api/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {item["id"]: item["is_active"] for item in response.data},
            {active.id: True, hidden.id: False},
        )
