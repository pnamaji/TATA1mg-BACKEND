# Generated by Django 4.2.16 on 2024-11-15 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Health_Plans', '0009_usercontact_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
    ]