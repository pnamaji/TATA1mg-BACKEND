# Generated by Django 4.2.16 on 2024-11-15 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Health_Checkup', '0007_testdetail_alter_health_packages_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testdetail',
            name='allowed_genders',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('BOTH', 'Both')], default='BOTH', max_length=5),
        ),
        migrations.AlterField(
            model_name='testdetail',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_details', to='Health_Checkup.health_packages'),
        ),
    ]