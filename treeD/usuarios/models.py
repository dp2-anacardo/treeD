from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    nombre = models.TextField(verbose_name='Nombre')
    apellidos = models.TextField(verbose_name='Apellidos')
    descripcion = models.TextField(verbose_name='Descripción', blank=True)
    email = models.EmailField(verbose_name='Email')
    imagen = models.ImageField(upload_to='', verbose_name='Imagen', default='default.png')
    es_afiliado = models.BooleanField(verbose_name='Afiliado?')
    
    def __str__(self):
        return self.usuario.username
    
    class Meta:
        ordering = ('pk', )


class DirecPerfil(models.Model):
    direccion = models.TextField(verbose_name='Dirección')
    perfil = models.ForeignKey('Perfil', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.direccion

    class Meta:
        ordering = ('pk',)