# Generated by Django 3.0.3 on 2020-03-16 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200315_2226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagen',
            name='compra',
        ),
        migrations.AddField(
            model_name='compra',
            name='imagenes',
            field=models.ManyToManyField(related_name='imagenes', to='main.Imagen'),
        ),
    ]
