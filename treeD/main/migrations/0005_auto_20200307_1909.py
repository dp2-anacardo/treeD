# Generated by Django 3.0.3 on 2020-03-07 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200307_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='imagen',
            field=models.ImageField(upload_to='imagenes', verbose_name='Imagen'),
        ),
    ]
