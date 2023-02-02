from django.shortcuts import render, redirect
import requests
import json

from .models import Item, TableSetting, BlackList

def index(request):
    #_fillUrls(Item.objects.all())

    table_settings = TableSetting.objects.get(id=1)
    black_list = BlackList.objects.all()

    items = [item for item in Item.objects.order_by('price').values('name', 'price', 'accuracy', 'image_url') 
        if (not(item['price'] == 0) or table_settings.zero_price_items) and item['name'] not in [bl_item.item.name for bl_item in black_list]]

    context = {}
    context['products'] = items[:10]
    context['qs_json'] = json.dumps({
        'data': items,
        })

    if(request.GET.get('mybtn')):
        updateDataBase()
        return redirect('index')
    
    if(request.GET.get('toindex')):
        return redirect('index')
    
    if(request.GET.get('toblacklist')):
        return redirect('black_list')
    
    print(request.path)
    
    return render(request, 'buylist/index.html', context)

def black_list(request):
    black_list = BlackList.objects.order_by('date_added')
    context = {}
    context['black_list'] = black_list

    if(request.GET.get('toindex')):
        return redirect('index')
    
    if(request.GET.get('toblacklist')):
        return redirect('black_list')

    return render(request, 'buylist/black_list.html', context)

def updateDataBase():
    req = requests.get('https://api.hypixel.net/skyblock/bazaar')
    products = getBuyOutList(json.loads(req.text)['products'])

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

    return {'price': int(price), 'accuracy' : f"{round(accuracy*100, 2)}%", 'min_price' : min_price}

def _fillUrls(items):
    urls, special = _getImages()
    for item in items:
        name = ([item.name] if all([spec_item not in item.name for spec_item in special]) else [spec_item for spec_item in special if spec_item in item.name])[0]
        try:
            url = urls[name]
        except:
            url = 'https://static.wikia.nocookie.net/minecraft/images/8/8d/BarrierNew.png/revision/latest?cb=20190830230156'
        item.image_url = url
        item.save()

def _getImages():
    urls = {
        'ENCHANTMENT': 'https://wiki.hypixel.net/images/4/4e/SkyBlock_items_enchanted_book.gif',
        'LOG':'https://wiki.hypixel.net/images/8/8d/Minecraft_items_oak_log.png',

        'ENDSTONE_GEODE': 'https://wiki.hypixel.net/images/2/2d/SkyBlock_items_endstone_geode.png',
        'PREMIUM_FLESH': 'https://wiki.hypixel.net/images/6/64/SkyBlock_items_premium_flesh.png',
        'ONYX': 'https://wiki.hypixel.net/images/3/33/SkyBlock_items_onyx.png',
        'RARE_DIAMOND':'https://wiki.hypixel.net/images/c/c4/SkyBlock_items_rare_diamond.png',
        'LAPIS_CRYSTAL':'https://wiki.hypixel.net/images/a/a7/SkyBlock_items_lapis_crystal.png',
        'REDSTONE':'https://wiki.hypixel.net/images/8/87/Minecraft_items_redstone_dust.png',
        'RABBIT_FOOT':'https://wiki.hypixel.net/images/7/7e/Minecraft_items_rabbits_foot.png',
        'ROUGH_TOPAZ_GEM':'https://wiki.hypixel.net/images/b/b8/SkyBlock_items_rough_ruby_gem.png',
        'CANDY_CORN':'https://wiki.hypixel.net/images/2/2f/SkyBlock_items_candy_corn.png',
        'SALMON_OPAL':'https://wiki.hypixel.net/images/0/00/SkyBlock_items_salmon_opal.png',
        'MINNOW_BAIT':'https://wiki.hypixel.net/images/c/c4/SkyBlock_items_minnow_bait.png',
        'ROUGH_AMETHYST_GEM':'https://wiki.hypixel.net/images/0/00/SkyBlock_items_rough_amethyst_gem.png',
        'BONE':'https://wiki.hypixel.net/images/7/7b/Minecraft_items_bone.png',
        'ROUGH_JADE_GEM':'https://wiki.hypixel.net/images/a/ad/SkyBlock_items_rough_jade_gem.png',
        'SAND':'https://wiki.hypixel.net/images/c/c8/Minecraft_items_sand.png',
        'WHEAT':'https://wiki.hypixel.net/images/4/4e/Minecraft_items_wheat.png',
        'MOLTEN_CUBE':'https://wiki.hypixel.net/images/1/15/SkyBlock_items_molten_cube.png',
        'SPIDER_EYE':'https://wiki.hypixel.net/images/a/ab/Minecraft_items_spider_eye.png',
        'RED_NOSE':'https://wiki.hypixel.net/images/3/36/SkyBlock_items_red_nose.png',
        'SEEDS':'https://wiki.hypixel.net/images/9/9b/Minecraft_items_wheat_seeds.png',
        'ENDER_MONOCLE':'https://wiki.hypixel.net/images/4/43/SkyBlock_items_ender_monocle.png',
        'POTATO_ITEM':'https://wiki.hypixel.net/images/d/d1/Minecraft_items_potato.png',
        'ENCHANTED_EGG':'https://wiki.hypixel.net/images/a/a1/SkyBlock_items_enchanted_egg.gif',
        'ENCHANTED_BREAD':'https://wiki.hypixel.net/images/8/88/SkyBlock_items_enchanted_bread.gif',
        'LUXURIOUS_SPOOL':'https://wiki.hypixel.net/images/a/a4/SkyBlock_items_luxurious_spool.png',
        'FLINT':'https://wiki.hypixel.net/images/e/ed/Minecraft_items_flint.png',
        'ROUGH_OPAL_GEM':'https://wiki.hypixel.net/images/f/fd/SkyBlock_items_rough_opal_gem.png',
        'GOBLIN_EGG_GREEN':'https://wiki.hypixel.net/images/4/45/Minecraft_items_egg.png',
        'END_STONE_SHULKER':'https://wiki.hypixel.net/images/c/c4/SkyBlock_items_end_stone_shulker.png',
        'ROUGH_SAPPHIRE_GEM':'https://wiki.hypixel.net/images/7/78/SkyBlock_items_rough_sapphire_gem.png',
        'ROUGH_JASPER_GEM':'https://wiki.hypixel.net/images/6/6f/SkyBlock_items_rough_jasper_gem.png',
        'MAGMA_FISH':'https://wiki.hypixel.net/images/5/52/SkyBlock_items_magma_fish.png',
        'MAGMA_CREAM':'https://wiki.hypixel.net/images/7/7e/Minecraft_items_magma_cream.png',
        'EXP_BOTTLE':'https://wiki.hypixel.net/images/6/6a/Minecraft_items_exp_bottle.png',
        'LIGHT_BAIT':'https://wiki.hypixel.net/images/4/40/SkyBlock_items_light_bait.png',
        'OPTICAL_LENS':'https://wiki.hypixel.net/images/5/5d/SkyBlock_items_optical_lens.png',
        'ICE_HUNK':'https://wiki.hypixel.net/images/b/bd/SkyBlock_items_ice_hunk.png',
        'DRAGON_SCALE':'https://wiki.hypixel.net/images/c/c7/SkyBlock_items_dragon_scale.png',
        'DARK_ORB': 'https://wiki.hypixel.net/images/e/ed/SkyBlock_items_dark_orb.png',
    }

    special = [
        'ENCHANTMENT', 
        'LOG',
    ]
    return urls, special