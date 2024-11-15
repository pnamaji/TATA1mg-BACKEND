# Generated by Django 4.2.16 on 2024-11-13 09:49

import Products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0004_remove_product_category_remove_product_categorytype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=Products.models.file_upload_to_brand),
        ),
        migrations.AlterField(
            model_name='category',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=Products.models.file_upload_to_category),
        ),
        migrations.AlterField(
            model_name='typesofcategory',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=Products.models.file_upload_to_categorytype),
        ),
    ]
