# Generated by Django 4.2.1 on 2023-06-10 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=9),
        ),
        migrations.AlterField(
            model_name='user',
            name='street',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='zip_code',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
