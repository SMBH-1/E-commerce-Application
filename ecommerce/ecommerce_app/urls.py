from django.urls import path
from .views import *
urlpatterns = [
  path('', index, name='index'),
  
  path('category/<str:category_str>/', category_detail, name='category_detail'),
  path('product/<int:product_id>/', product_detail, name='product_detail'),
  
  path('shopping-cart/', shopping_cart, name='shopping_cart'),
  path('add-product/<int:product_id>/', add_product),
  
  path('search/', search, name='search'),
  path('search/<str:search_string>/', search_results, name='search_results')
]