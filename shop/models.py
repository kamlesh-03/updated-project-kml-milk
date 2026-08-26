from django.conf import settings
from django.db import models
from django.utils import timezone

class Category(models.Model):
    slug = models.SlugField(unique=True)
    name_en = models.CharField(max_length=100)
    name_mr = models.CharField(max_length=100, blank=True)
    name_hi = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name_en

    def localized_name(self, lang):
        return getattr(self, f"name_{lang}", None) or self.name_en

class Product(models.Model):
    FAT = "fat"
    FRESH = "fresh"
    ICECREAM = "icecream"
    SECTION_CHOICES = [
        (FAT, "Butter, Ghee & Cheese"),
        (FRESH, "Fresh Milk & Curd"),
        (ICECREAM, "Dudhbar Ice Cream"),
    ]

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    pack_size = models.CharField(max_length=30)
    unit = models.CharField(max_length=10, default="g")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    market_rate_note = models.CharField(max_length=255, blank=True)
    stock_qty = models.PositiveIntegerField(default=0)
    expiry_days = models.PositiveIntegerField(default=7)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    usage = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def expiry_date(self):
        return timezone.localdate() + timezone.timedelta(days=self.expiry_days)

    def __str__(self):
        return f"{self.name} - {self.pack_size}{self.unit}"

class FarmContent(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image_url = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    STATUS = [
        ("new", "New"),
        ("confirmed", "Confirmed"),
        ("packed", "Packed"),
        ("out", "Out for delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
