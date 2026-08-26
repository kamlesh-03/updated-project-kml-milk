import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, FarmContent, Order, OrderItem

def home(request):
    sections = [
        {"slug": "fat", "title": "Butter • Ghee • Cheese", "text": "Rich dairy products from 100g to 950g."},
        {"slug": "fresh", "title": "Fresh Milk • Curd", "text": "Daily fresh products from 200ml to 960ml."},
        {"slug": "icecream", "title": "Dudhbar by KML Agro Farms", "text": "Ice cream supply for nearby shops and grocery stores."},
    ]
    return render(request, "home.html", {"sections": sections})

def section(request, section):
    products = Product.objects.filter(section=section, active=True).select_related("category")
    title_map = {"fat": "Butter, Ghee & Cheese", "fresh": "Fresh Milk & Curd", "icecream": "Dudhbar by KML Agro Farms"}
    return render(request, "shop/section.html", {"products": products, "title": title_map.get(section, section.title())})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    whatsapp = f"https://wa.me/919923573738?text=Hello%20KML%20Milk%2C%20I%20want%20to%20order%20{product.name}%20{product.pack_size}{product.unit}."
    return render(request, "shop/product_detail.html", {"product": product, "whatsapp": whatsapp})

def order_create(request):
    if request.method != "POST":
        return redirect("home")
    data = request.POST
    try:
        items = json.loads(data.get("items", "[]"))
    except json.JSONDecodeError:
        items = []
    order = Order.objects.create(
        customer=request.user if request.user.is_authenticated else None,
        name=data.get("name", ""),
        phone=data.get("phone", ""),
        email=data.get("email", ""),
        address=data.get("address", ""),
        notes=data.get("notes", ""),
    )
    for item in items:
        try:
            product = Product.objects.get(id=int(item["product_id"]), active=True)
            qty = max(1, int(item.get("quantity", 1)))
            OrderItem.objects.create(order=order, product=product, quantity=qty, unit_price=product.price)
        except (Product.DoesNotExist, ValueError, KeyError):
            continue
    messages.success(request, f"Order #{order.id} received. Our team will contact you.")
    return redirect("home")

def farm(request):
    posts = FarmContent.objects.filter(active=True).order_by("-published_at")
    return render(request, "farm.html", {"posts": posts})

def contact(request):
    return render(request, "contact.html")

def health(request):
    return JsonResponse({"status": "UP", "service": "kml-milk"})
