from django.contrib import admin
from .models import Item, TableSetting, BlackList

admin.site.register(Item)
admin.site.register(TableSetting)
admin.site.register(BlackList)
