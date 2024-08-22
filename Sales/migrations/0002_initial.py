# Generated by Django 5.0.8 on 2024-08-22 02:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Sales', '0001_initial'),
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_customer', to='User.customer', verbose_name='customer'),
        ),
        migrations.AddField(
            model_name='sales',
            name='items',
            field=models.ManyToManyField(related_name='items', to='Sales.items', verbose_name='items'),
        ),
    ]
