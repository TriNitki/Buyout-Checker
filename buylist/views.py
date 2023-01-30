from django.shortcuts import render, redirect
from requests import get
import json

from .models import Item, TableSetting, BlackList

def index(request):
    
    table_settings = TableSetting.objects.get(id=1)
    black_list = BlackList.objects.all()

    req = get('https://api.hypixel.net/skyblock/bazaar')
    products = getBuyOutList(json.loads(req.text)['products'])

    items = [item for item in Item.objects.order_by('price').values('name', 'price', 'accuracy') 
        if (not(item['price'] == 0) or table_settings.zero_price_items) and item['name'] not in [bl_item.item.name for bl_item in black_list]]

    context = {}
    context['products'] = items[:10]
    context['qs_json'] = json.dumps({
        'data': items,
        })
    
    if(request.GET.get('mybtn')):
        updateDataBase(products)
        return redirect('index')
    
    return render(request, 'buylist/index.html', context)

def updateDataBase(products):
    for product in products:
        item = Item.objects.get(name=product['name'])
        item.accuracy = product['accuracy']
        item.price = product['price']
        item.min_price = product['min_price']
        item.save()

def getBuyOutList(products):
    product_id = products.keys()
    result = []
    for product in product_id:
        product_info = getProductInfo(products[product])
        product_info['name'] = product
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
        accuracy = amount / product['quick_status']['buyVolume']

    return {'price': round(price), 'accuracy' : f"{round(accuracy*100, 2)}%", 'min_price' : min_price}