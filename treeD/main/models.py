from django.db import models
from django.contrib.auth.models import User


class Impresion(models.Model):
    idImpresion = models.AutoField(primary_key=True)
    nombre = models.TextField(verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción') 
    precio = models.TextField(verbose_name='Precio')
    imagen = models.URLField(verbose_name = 'Imagen')
    vendedor = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('idImpresion', )




class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    impresionesCompradas = models.ManyToManyField(Impresion, blank=True)
    usuario = models.OneToOneField(User,on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.idUsuario
    
    class Meta:
        ordering = ('idUsuario', )
        

