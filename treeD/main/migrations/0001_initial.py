# Generated by Django 3.0.3 on 2020-03-16 14:19

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
            name='Categoria',
            fields=[
                ('idCategoria', models.AutoField(primary_key=True, serialize=False)),
                ('categoria', models.TextField(verbose_name='Categoría')),
            ],
            options={
                'ordering': ('idCategoria',),
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('idPerfil', models.AutoField(primary_key=True, serialize=False)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('idPerfil',),
            },
        ),
        migrations.CreateModel(
            name='Impresion',
            fields=[
                ('idImpresion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('precio', models.FloatField(verbose_name='Precio')),
                ('categorias', models.ManyToManyField(to='main.Categoria')),
                ('vendedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Perfil')),
            ],
            options={
                'ordering': ('idImpresion',),
            },
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('idImagen', models.AutoField(primary_key=True, serialize=False)),
                ('imagen', models.ImageField(upload_to='imagenes', verbose_name='Imagen')),
                ('impresion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Impresion')),
            ],
            options={
                'ordering': ('idImagen',),
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('idCompra', models.AutoField(primary_key=True, serialize=False)),
                ('nombreImpresion', models.TextField(blank=True, verbose_name='Nombre de la impresión')),
                ('descripcionImpresion', models.TextField(blank=True, verbose_name='Descripción de la impresión')),
                ('precioImpresion', models.FloatField(null=True, verbose_name='Precio de la impresión')),
                ('fechaDeCompra', models.DateField(verbose_name='Fecha de compra')),
                ('comprador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comprador', to='main.Perfil')),
                ('imagenes', models.ManyToManyField(to='main.Imagen', verbose_name='Imagenes')),
                ('vendedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendedor', to='main.Perfil')),
            ],
            options={
                'ordering': ('idCompra', 'fechaDeCompra'),
            },
        ),
    ]
