# Generated by Django 4.1.5 on 2023-01-29 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buylist', '0009_rename_name_blacklist_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklist',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='buylist.item'),
        ),
    ]