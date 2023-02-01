# Generated by Django 4.1.5 on 2023-02-01 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buylist', '0010_alter_blacklist_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='blacklist',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buylist.item'),
        ),
    ]
