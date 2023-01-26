from django.shortcuts import render
from requests import get
from json import loads

from .models import Item

def index(request):
    req = get('https://api.hypixel.net/skyblock/bazaar')

    products = getBuyOutList(loads(req.text)['products'])
    
    Item.objects.all().delete()

    for product in products:
        obj = Item()
        obj.name = product['name']
        obj.price = product['price']
        obj.accuracy = product['accuracy']
        obj.min_price = product['min_price']
        obj.save()

    products = Item.objects.order_by('price')

    context = {'products': products}
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

    return {'price': round(price), 'accuracy' : accuracy, 'min_price' : min_price}