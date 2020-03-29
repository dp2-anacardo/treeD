# Generated by Django 3.0.3 on 2020-03-29 18:10

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_impresion', models.TextField(blank=True, verbose_name='Nombre de la impresión')),
                ('desc_impresion', models.TextField(blank=True, verbose_name='Descripción de la impresión')),
                ('precio_impresion', models.FloatField(null=True, verbose_name='Precio de la impresión')),
                ('fecha_compra', models.DateField(verbose_name='Fecha de compra')),
            ],
            options={
                'ordering': ('pk', 'fecha_compra'),
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('apellidos', models.TextField(verbose_name='Apellidos')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('imagen', models.ImageField(default='default.png', upload_to='', verbose_name='Imagen')),
                ('es_afiliado', models.BooleanField(verbose_name='Afiliado?')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peticion', models.TextField(verbose_name='Peticion')),
                ('descripcion', models.TextField(verbose_name='Descripcion')),
                ('precio', models.FloatField(null=True, verbose_name='Precio')),
                ('notas', models.TextField(null=True, verbose_name='Notas')),
                ('fecha_envio', models.DateField(null=True, verbose_name='Fecha de envio')),
                ('resp_interesado', models.BooleanField(null=True, verbose_name='Respuesta del Interesado')),
                ('resp_vendedor', models.BooleanField(null=True, verbose_name='Respuesta del Vendedor')),
                ('interesado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Interesado', to='main.Perfil')),
                ('vendedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Vendedor', to='main.Perfil')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Impresion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('precio', models.FloatField(verbose_name='Precio')),
                ('categorias', models.ManyToManyField(to='main.Categoria')),
                ('vendedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Perfil')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='ImgPrueba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='', verbose_name='Imagen')),
                ('compra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Compra')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='ImgImpresion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='', verbose_name='Imagen')),
                ('impresion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Impresion')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='ImgCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='', verbose_name='Imagen')),
                ('compra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Compra')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='DirecPerfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.TextField(verbose_name='Dirección')),
                ('perfil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Perfil')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.AddField(
            model_name='compra',
            name='comprador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comprador', to='main.Perfil'),
        ),
        migrations.AddField(
            model_name='compra',
            name='direccion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.DirecPerfil'),
        ),
        migrations.AddField(
            model_name='compra',
            name='vendedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendedor', to='main.Perfil'),
        ),
    ]
