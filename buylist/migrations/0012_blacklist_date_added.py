# Generated by Django 4.1.5 on 2023-02-02 10:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('buylist', '0011_item_image_url_alter_blacklist_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='blacklist',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
