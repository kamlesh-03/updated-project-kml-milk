from django.test import TestCase
from django.urls import reverse
from .models import Category, Product

class ShopTests(TestCase):
    def setUp(self):
        c = Category.objects.create(slug="fresh", name_en="Fresh Dairy")
        Product.objects.create(
            category=c, name="Fresh Milk", slug="fresh-milk",
            section="fresh", pack_size="500", unit="ml",
            price=50, stock_qty=20, expiry_days=2, active=True
        )

    def test_home(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_health(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "UP", "service": "kml-milk"})
