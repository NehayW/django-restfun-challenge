# Generated by Django 3.2.12 on 2022-02-03 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0004_order_total_bill'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='option',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
