# Generated by Django 5.0 on 2024-01-08 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Branch Name')),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='Branch_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_product_branch', to='Branch.branch', verbose_name='branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_product_product', to='Product.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Branch_Product',
                'verbose_name_plural': 'Branch_Products',
            },
        ),
        migrations.CreateModel(
            name='Branch_Suit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Branch_Suit_branch', to='Branch.branch', verbose_name='branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Branch_Suit_product', to='Product.suit', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Branch_Suit',
                'verbose_name_plural': 'Branch_Suits',
            },
        ),
        migrations.CreateModel(
            name='Branch_Tops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Branch_Tops_branch', to='Branch.branch', verbose_name='branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Branch_Tops_product', to='Product.top', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Branch_Tops',
                'verbose_name_plural': 'Branch_Tops',
            },
        ),
        migrations.CreateModel(
            name='Product_Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_qty', models.IntegerField(default=0, verbose_name='current_qty')),
                ('returned_qty', models.IntegerField(default=0, verbose_name='returned_qty')),
                ('bad_qty', models.IntegerField(default=0, verbose_name='bad_qty')),
                ('branch_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Branch.branch_product', verbose_name='branch_product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_product_sizes', to='Product.size')),
            ],
            options={
                'verbose_name': 'product_Size',
                'verbose_name_plural': 'product_Sizes',
            },
        ),
        migrations.CreateModel(
            name='Suit_Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_qty', models.IntegerField(default=0, verbose_name='current_qty')),
                ('returned_qty', models.IntegerField(default=0, verbose_name='returned_qty')),
                ('bad_qty', models.IntegerField(default=0, verbose_name='bad_qty')),
                ('branch_suit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Branch.branch_suit', verbose_name='Branch_Suit')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Branch_Suit_sizes', to='Product.size')),
            ],
            options={
                'verbose_name': 'Suit_size',
                'verbose_name_plural': 'Suit_sizes',
            },
        ),
        migrations.CreateModel(
            name='Tops_Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_qty', models.IntegerField(default=0, verbose_name='current_qty')),
                ('returned_qty', models.IntegerField(default=0, verbose_name='returned_qty')),
                ('bad_qty', models.IntegerField(default=0, verbose_name='bad_qty')),
                ('branch_tops', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Branch.branch_tops', verbose_name='Branch_Tops')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Branch_Tops_sizes', to='Product.size')),
            ],
            options={
                'verbose_name': 'Top_Size',
                'verbose_name_plural': 'Top_Sizes',
            },
        ),
    ]
