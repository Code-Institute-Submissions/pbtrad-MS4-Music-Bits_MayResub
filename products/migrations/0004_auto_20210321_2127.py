# Generated by Django 3.1.7 on 2021-03-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210321_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='has_sizes',
            field=models.BooleanField(blank=True, default=False, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='string_gauge',
            field=models.BooleanField(blank=True, default=False, max_length=254, null=True),
        ),
    ]