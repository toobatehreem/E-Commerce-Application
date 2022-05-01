from re import I
from unicodedata import name
from django.urls import path
from . import views
from .views import Kurti_Index, Trousers_Index, Cart, CheckOut, Index

app_name = 'App'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', views.loginuser, name='login'),
    path('register/', views.register, name='register'),
    path("logout", views.logoutuser, name= "logout"),
    path("categories/", views.categories, name= "categories"),
    path("categories/Kurti/", Kurti_Index.as_view(), name= "kurti"),
    path("categories/Trousers/", Trousers_Index.as_view(), name= "trousers"),
    path("cart", Cart.as_view(), name= "cart"),
    path("checkout", CheckOut.as_view(), name= "checkout"),
    path("add_products", views.add_products, name='add_products'),
    path("see_orders", views.see_orders, name='see_orders')
    
]