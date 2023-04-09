from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .csv_interface import CSV_Interface
import requests as HttpClient
from collections import Counter
from requests_oauthlib import OAuth1
import pprint
from dotenv import load_dotenv
import os

load_dotenv()
pp = pprint.PrettyPrinter(indent=2, depth=2)
products_interface = CSV_Interface('./ecommerce_app/data/products.csv')
shopping_cart_interface = CSV_Interface('./ecommerce_app/data/shopping_cart.csv')

#Takes products.csv and returns dictionary of categories accounting for duplicates
def index(request): 
  all_products = products_interface.all_data
  print(all_products)
  home_page_categories = []
  for product in all_products:
    if product['category'] not in home_page_categories:
      home_page_categories.append(product['category'])
  categories_dict = {'categories': home_page_categories}
  return render(request, 'ecommerce_app/index.html', categories_dict)


#Takes in category string and uses products.csv to return dict of products in specified category
def category_detail(request, category_str): 
  products = products_interface.all_data
  category_data = []
  for product in products:
    if product['category'] == category_str:
      category_data.append({'id': product['id'], 'name': product['name']})
  category_dict = {'category_data': category_data}
  return render(request, 'ecommerce_app/category_detail.html', category_dict)

#Takes in unique product id and uses products.csv to return dict of the specified product's details
def product_detail(request, product_id):   
  all_products = products_interface.all_data
  for product in all_products:
    if product['id'] == str(product_id):
      data = {'id': product['id'], 'name': product['name'], 'category':product['category'], 'cost': product['cost'], 'image_url': product['image_url']}
  return render(request, 'ecommerce_app/product_detail.html', data)
  
#Uses shopping_cart.csv and compares to products.csv to combine similar products, totaling quantity and cost present in shopping cart.  
#Product name, total product quantity, combined product cost, and all items cost put into list and pushed to render function.
def shopping_cart(request):
  existing_cart = shopping_cart_interface.all_data
  product_list = products_interface.all_data
  total_sum = 0
  updated_list = []
  result = Counter()
  
  for item in existing_cart:
    ID = int(item['id'])
    quantity_int = int(item['quantity'])
    result[ID] += quantity_int
  
  for elem in result:
    for product in product_list:
      if elem == int(product['id']):
        cost = int(product['cost'])*result[elem]
        total_sum += cost
        data = {'id': product['id'], 'name' : product['name'], 'quantity' : result[elem], 'cost' : cost}
        updated_list.append(data)
  updated_list.append({'total_sum':total_sum})

  return render(request, 'ecommerce_app/shopping_cart.html', {'mod': updated_list})


#Adds specified product to products.csv when 'Add to Cart' button clicked on product_detail.html
def add_product(request, product_id):
  if request.method == 'POST':
    shopping_cart_interface.append_one_row_to_file({'id': product_id, 'quantity': 1})
  return HttpResponseRedirect('/shopping-cart/')

#Renders search page to look up products
def search(request):
  return render(request, 'ecommerce_app/search.html')

#Returns search results for products. If item exists in store, search redirects to specific product. 
# If item does not exist in store, renders search_results.html notifying product out of stock.
def search_results(request, search_string):
  auth = OAuth1(os.environ['api_key'],os.environ['secret_key'])
  try:
    endpoint = f"http://api.thenounproject.com/icon/{search_string}"
    response = HttpClient.get(endpoint, auth=auth)
    response_json = response.json()
    url = response_json['icon']['preview_url']
    all_products = products_interface.all_data
    search_string = search_string.lower()
    
    for product in all_products:
      if product['name'] == search_string:
        return HttpResponseRedirect('/product/%s' % product['id'])
    return render(request, 'ecommerce_app/search_results.html', {'image_url': url})

  except ValueError: #If search string value does not produce image from The Noun Project API, returns error message
    error_msg = 'We may not carry this item'
    return render(request, 'ecommerce_app/search_results.html', {'em':error_msg} )