# Generated by Django 4.2.16 on 2024-11-10 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address_type',
            field=models.CharField(choices=[('home', 'Home'), ('office', 'Office'), ('other', 'Other')], default='home', max_length=10),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='customer',
            name='zipcode',
            field=models.CharField(max_length=10),
        ),
    ]
