# Generated by Django 5.0 on 2024-02-13 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Branch', '0001_initial'),
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Foot_Wear_Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(verbose_name='qty')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foot_wear_stock_branch', to='Branch.branch', verbose_name='branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foot_wear_stock', to='Product.foot_wear', verbose_name='foot_wear')),
                ('size_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foot_wear_stock_size_instance', to='Product.size', verbose_name='size_instance')),
            ],
            options={
                'verbose_name': 'Foot_Wear_Stock',
                'verbose_name_plural': 'Foot_Wear_Stocks',
            },
        ),
        migrations.CreateModel(
            name='Product_Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(verbose_name='qty')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_stock_branch', to='Branch.branch', verbose_name='branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_stock', to='Product.product', verbose_name='product')),
                ('size_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_stock_size_instance', to='Product.size', verbose_name='size_instance')),
            ],
            options={
                'verbose_name': 'Product Stock',
                'verbose_name_plural': 'Product Stocks',
            },
        ),
        migrations.CreateModel(
            name='Suit_Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(verbose_name='qty')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suit_stock_branch', to='Branch.branch', verbose_name='branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suit_stock', to='Product.suit', verbose_name='suit')),
                ('size_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suit_stock_size_instance', to='Product.size', verbose_name='size_instance')),
            ],
            options={
                'verbose_name': 'Suit Stock',
                'verbose_name_plural': 'Suit Stocks',
            },
        ),
        migrations.CreateModel(
            name='Tops_Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(verbose_name='qty')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tops_stock_branch', to='Branch.branch', verbose_name='branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='top_stock', to='Product.top', verbose_name='tops')),
                ('size_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tops_stock_size_instance', to='Product.size', verbose_name='size_instance')),
            ],
            options={
                'verbose_name': 'Tops Stock',
                'verbose_name_plural': 'Tops Stocks',
            },
        ),
    ]
