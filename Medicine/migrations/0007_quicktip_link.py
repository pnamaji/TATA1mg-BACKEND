# Generated by Django 4.2.16 on 2024-11-19 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Medicine', '0006_quicktip_medicine'),
    ]

    operations = [
        migrations.AddField(
            model_name='quicktip',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]