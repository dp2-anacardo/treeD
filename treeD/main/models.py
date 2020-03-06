from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nombre = models.TextField(verbose_name='Categoría', unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('idCategoria', )



class Impresion(models.Model):
    idImpresion = models.AutoField(primary_key=True)
    nombre = models.TextField(verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción') 
    precio = models.FloatField(verbose_name='Precio')
    imagen = models.ImageField(verbose_name = 'Imagen')
    publicador = models.ForeignKey('Perfil', on_delete=models.SET_NULL, null=True)
    categorias = models.ManyToManyField(Categoria)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('idImpresion', )




class Perfil(models.Model):
    idPerfil = models.AutoField(primary_key=True)
    impresionesCompradas = models.ManyToManyField(Impresion, through='Compra', blank=True)
    usuario = models.OneToOneField(User,on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.usuario.username
    
    class Meta:
        ordering = ('idPerfil', )
        


class Compra(models.Model):
    idCompra = models.AutoField(primary_key=True)
    idPerfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    idImpresion = models.ForeignKey(Impresion, on_delete=models.CASCADE)
    fechaDeCompra = models.DateField(verbose_name="Fecha de compra")

    def __str__(self):
        return str(self.fechaDeCompra)

    class Meta:
        ordering = ('idCompra', 'fechaDeCompra', )

