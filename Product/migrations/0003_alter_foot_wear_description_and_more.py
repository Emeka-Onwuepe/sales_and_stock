# Generated by Django 5.0.2 on 2024-03-03 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_alter_foot_wear_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foot_wear',
            name='description',
            field=models.TextField(blank=True, max_length=150, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, max_length=150, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='suit',
            name='description',
            field=models.TextField(blank=True, max_length=150, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='top',
            name='description',
            field=models.TextField(blank=True, max_length=150, null=True, verbose_name='description'),
        ),
    ]
