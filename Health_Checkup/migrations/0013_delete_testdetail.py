# Generated by Django 4.2.16 on 2024-11-15 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Health_Checkup', '0012_testdetail_name_alter_testdetail_allowed_genders'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestDetail',
        ),
    ]
