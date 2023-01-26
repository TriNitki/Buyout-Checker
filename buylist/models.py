from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    min_price = models.FloatField()
    accuracy = models.CharField(max_length=5)

    def __str__(self) -> str:
        return self.name

class TableSetting(models.Model):
    zero_price_items = models.BooleanField()
    max_prod_amount = models.IntegerField()

    def __str__(self) -> str:
        return "Main settings!"