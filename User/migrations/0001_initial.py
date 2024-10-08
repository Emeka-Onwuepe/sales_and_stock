# Generated by Django 5.0.8 on 2024-08-22 02:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Branch', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(max_length=20, unique=True, verbose_name='phone_number')),
                ('address', models.CharField(max_length=256, verbose_name='address')),
                ('total_credit', models.IntegerField(default=0, verbose_name='total_credit')),
                ('total_payment', models.IntegerField(default=0, verbose_name='total_payment')),
                ('balance', models.IntegerField(default=0, verbose_name='total_balance')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('full_name', models.CharField(max_length=255, verbose_name='full name')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='phone_number')),
                ('is_super_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branch', to='Branch.branch', verbose_name='branch')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
