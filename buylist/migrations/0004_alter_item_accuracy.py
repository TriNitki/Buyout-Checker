# Generated by Django 4.1.5 on 2023-01-26 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buylist', '0003_rename_buyout_price_item_price_alter_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='accuracy',
            field=models.CharField(max_length=5),
        ),
    ]