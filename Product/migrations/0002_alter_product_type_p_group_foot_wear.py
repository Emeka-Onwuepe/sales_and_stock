# Generated by Django 5.0 on 2024-01-15 21:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_type',
            name='p_group',
            field=models.CharField(choices=[('suits', 'suits'), ('foot_wear', 'foot_wear'), ('top', 'top'), ('product', 'product')], default='product', max_length=10),
        ),
        migrations.CreateModel(
            name='Foot_Wear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=150, verbose_name='description')),
                ('color', models.CharField(max_length=200, verbose_name='color')),
                ('image', models.ImageField(blank=True, default='image', null=True, upload_to='', verbose_name='image')),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('U', 'Unisex')], default='U', max_length=2)),
                ('age_group', models.CharField(choices=[('A', 'Adult'), ('C', 'Children')], default='A', max_length=2)),
                ('brand', models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='brand')),
                ('type', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='type')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('publish', models.BooleanField(default=False)),
                ('sole_color', models.CharField(blank=True, default=None, max_length=25, null=True, verbose_name='Sole Color')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foot_wear_product_type', to='Product.product_type')),
                ('sizes', models.ManyToManyField(blank=True, related_name='foot_wear_sizes', to='Product.size', verbose_name='sizes')),
            ],
            options={
                'verbose_name': 'Foot_Wear',
                'verbose_name_plural': 'Foot_Wears',
                'ordering': ['-date'],
            },
        ),
    ]
