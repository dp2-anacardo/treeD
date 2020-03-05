# Generated by Django 3.0.3 on 2020-03-05 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Impresion',
            fields=[
                ('idImpresion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('precio', models.TextField(verbose_name='Precio')),
                ('imagen', models.URLField(verbose_name='Imagen')),
            ],
            options={
                'ordering': ('idImpresion',),
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('idUsuario', models.AutoField(primary_key=True, serialize=False)),
                ('impresionesCompradas', models.ManyToManyField(blank=True, to='main.Impresion')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('idUsuario',),
            },
        ),
        migrations.AddField(
            model_name='impresion',
            name='vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Usuario'),
        ),
    ]
