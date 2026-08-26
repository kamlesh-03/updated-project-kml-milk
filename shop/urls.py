from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/<slug:section>/", views.section, name="section"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("order/", views.order_create, name="order_create"),
    path("farm/", views.farm, name="farm"),
    path("contact/", views.contact, name="contact"),
    path("health/", views.health, name="health"),
]
