# Generated by Django 5.0 on 2024-01-15 21:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Branch', '0005_branch_foot_wear_foot_wear_size'),
        ('Product', '0002_alter_product_type_p_group_foot_wear'),
        ('Returned_Product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Returned_Foot_Wear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(verbose_name='qty')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=50, verbose_name='unit_price')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=50, verbose_name='total_price')),
                ('date_of_purchase', models.DateField(verbose_name='date_of_purchase')),
                ('date_of_return', models.DateTimeField(verbose_name='date_of_return')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='returned_foot_wear_branch', to='Branch.branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='returned_foot_wear_product_type', to='Product.foot_wear', verbose_name='foot_wear')),
                ('size_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='returned_foot_wear_size_instance', to='Product.size', verbose_name='size_instance')),
            ],
            options={
                'verbose_name': 'Returned_Foot_Wear',
                'verbose_name_plural': 'Returned_Foot_Wears',
            },
        ),
    ]