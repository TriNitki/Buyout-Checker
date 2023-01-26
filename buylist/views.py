from django.shortcuts import render
from requests import get
from json import loads

from .models import Item

def index(request):
    req = get('https://api.hypixel.net/skyblock/bazaar')
    products = loads(req.text)['products']

    g_list = getBuyOutList(products)
    sorted_list = sorted(g_list, key=lambda prod: prod['price'])
    
    context = {'products': sorted_list[:10]}
    return render(request, 'buylist/index.html', context)

def getBuyOutList(products):
    product_id = products.keys()
    result = []
    for product in product_id:
        product_info = getProductInfo(products[product])
        product_info['name'] = product
        if product_info['price'] == 0:
            continue
        
        result.append(product_info)
    return result

def getProductInfo(product):
    price = 0
    amount = 0
    accuracy = 1
    max_price = 0

    try:
        min_price = product['buy_summary'][0]['pricePerUnit']
    except:
        min_price = 0
    
    for offer in product['buy_summary']:
        amount += offer['amount']
        price += offer['amount'] * offer['pricePerUnit']
        max_price = offer['pricePerUnit']
    
    if amount < product['quick_status']['buyVolume']:
        price += (product['quick_status']['buyVolume'] - amount) * max_price
        accuracy = f"{round(amount / product['quick_status']['buyVolume']*100, 2)}%"

    return {'price': price, 'accuracy' : accuracy, 'min_price' : min_price}