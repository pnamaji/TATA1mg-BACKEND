# Generated by Django 4.2.16 on 2024-11-20 15:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0013_producthighlight_product_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_on_sale',
            field=models.CharField(choices=[('null', 'Null'), ('sell', 'Sell'), ('best_seller', 'Best Seller')], default='null'),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='unit_type',
            field=models.CharField(choices=[('jar', 'Jar'), ('tube', 'Tube'), ('strip', 'Strip'), ('combo_pack', 'Combo Pack'), ('pump_bottle', 'Pump Bottle'), ('packet', 'Packet'), ('sachet', 'Sachet'), ('box', 'Box'), ('bottle', 'Bottle')], default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]