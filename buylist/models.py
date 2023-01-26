from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=50)
    buyout_price = models.FloatField()
    min_price = models.FloatField()
    accuracy = models.FloatField()

    def __str__(self) -> str:
        return self.name