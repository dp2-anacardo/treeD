from django.db import models
from django.contrib.auth.models import User

class ImgCompra(models.Model):
    imagen = models.ImageField(upload_to='', verbose_name='Imagen')
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.compra.nombre_impresion + self.compra.fecha_compra

    class Meta:
        ordering = ('pk',)

class ImgImpresion(models.Model):
    imagen = models.ImageField(upload_to='', verbose_name='Imagen')
    impresion = models.ForeignKey('Impresion', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.impresion.nombre

    class Meta:
        ordering = ('pk',)

class Categoria(models.Model):
    nombre = models.TextField(verbose_name='Nombre')

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('pk', )

class Impresion(models.Model):
    nombre = models.TextField(verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción')
    precio = models.FloatField(verbose_name='Precio')
    vendedor = models.ForeignKey('Perfil', on_delete=models.CASCADE, null=True)
    categorias = models.ManyToManyField('Categoria')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('pk', )

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.usuario.username
    
    class Meta:
        ordering = ('pk', )

class Compra(models.Model):
    comprador = models.ForeignKey(Perfil, related_name='comprador', on_delete=models.SET_NULL, null=True)
    vendedor = models.ForeignKey(Perfil, related_name='vendedor', on_delete=models.SET_NULL, null=True)
    nombre_impresion = models.TextField(verbose_name='Nombre de la impresión', blank=True)
    desc_impresion = models.TextField(verbose_name='Descripción de la impresión', blank=True)
    precio_impresion = models.FloatField(verbose_name='Precio de la impresión', null=True)
    fecha_compra = models.DateField(verbose_name="Fecha de compra")

    def __str__(self):
        return self.nombre_impresion + self.fecha_compra

    class Meta:
        ordering = ('pk', 'fecha_compra', )