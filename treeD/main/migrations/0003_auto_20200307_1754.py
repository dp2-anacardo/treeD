# Generated by Django 3.0.3 on 2020-03-07 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200307_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impresion',
            name='categorias',
            field=models.ManyToManyField(blank='False', to='main.Categoria'),
        ),
    ]
