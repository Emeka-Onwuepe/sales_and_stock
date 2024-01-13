# Generated by Django 5.0 on 2024-01-12 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Branch', '0002_alter_product_size_branch_product_and_more'),
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch_suit',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_suit_branch', to='Branch.branch', verbose_name='branch'),
        ),
        migrations.AlterField(
            model_name='branch_suit',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_suit_product', to='Product.suit', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='branch_tops',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_tops_branch', to='Branch.branch', verbose_name='branch'),
        ),
        migrations.AlterField(
            model_name='branch_tops',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_tops_product', to='Product.top', verbose_name='product'),
        ),
    ]