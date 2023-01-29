from django.shortcuts import render
from requests import get
import json

from .models import Item, TableSetting

def index(request):
    Item.objects.all().delete()
    table_settings = TableSetting.objects.get(id=1)

    req = get('https://api.hypixel.net/skyblock/bazaar')
    products = getBuyOutList(json.loads(req.text)['products'], table_settings)
    sorted_products = sorted(products, key=lambda prod: prod['price'])

    for product in sorted_products[:table_settings.max_items_amount]:
        obj = Item()
        obj.name = product['name']
        obj.price = product['price']
        obj.accuracy = product['accuracy']
        obj.min_price = product['min_price']
        obj.save()

    products = Item.objects.order_by('price')

    context = {'products': products}
    context["qs_json"] = json.dumps(list(Item.objects.values('name', 'price', 'accuracy')))
    return render(request, 'buylist/index.html', context)

def getBuyOutList(products, table_settings):
    product_id = products.keys()
    result = []
    for product in product_id:
        product_info = getProductInfo(products[product])
        product_info['name'] = product

        if product_info['price'] == 0 and not (table_settings.zero_price_items):
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