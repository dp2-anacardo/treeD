from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from statistics import mean
from math import ceil

class ImgPrueba(models.Model):
    imagen = models.ImageField(upload_to='', verbose_name='Imagen')
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.compra.nombre + str(self.compra.fecha_compra)

    class Meta:
        ordering = ('pk',)

class CodigoEnvio(models.Model):
    codigo_envio = models.TextField(verbose_name='Código de envío',null=True)
    empresa_envio = models.TextField(verbose_name='Empresa del envío')
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.empresa_envio + " " + self.codigo_envio

    class Meta:
        ordering = ('pk',)

class ImgCompra(models.Model):
    imagen = models.ImageField(upload_to='', verbose_name='Imagen')
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.compra.nombre + str(self.compra.fecha_compra)

    class Meta:
        ordering = ('pk',)

class ImgImpresion(models.Model):
    imagen = models.ImageField(upload_to='', verbose_name='Imagen')
    impresion = models.ForeignKey('Impresion', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.impresion.nombre

    class Meta:
        ordering = ('pk',)

class DirecPerfil(models.Model):
    ciudad = models.TextField(verbose_name='Ciudad')
    localidad = models.TextField(verbose_name='Localidad')
    calle = models.TextField(verbose_name='Calle o avenida')
    numero = models.TextField(verbose_name='número')
    codigo_postal = models.TextField(verbose_name='Código postal')
    perfil = models.ForeignKey('Perfil', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.ciudad + ', ' +self.localidad + ', ' +self.codigo_postal + '. ' +self.calle + ' ' +  self.numero

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
    nombre = models.TextField(verbose_name='Nombre')
    apellidos = models.TextField(verbose_name='Apellidos')
    descripcion = models.TextField(verbose_name='Descripción', blank=True)
    email = models.EmailField(verbose_name='Email')
    email_paypal = models.EmailField(verbose_name='Email de Paypal', null=True)
    imagen = models.ImageField(upload_to='', verbose_name='Imagen', default='default.png')
    es_afiliado = models.BooleanField(verbose_name='Afiliado?')

    @property
    def puntuacion(self):
        puntuaciones = Opinion.objects.filter(compra__vendedor=self).values('nota')
        if puntuaciones:
            puntuaciones_l = []
            for element in puntuaciones:
                puntuaciones_l.append(element['nota'])
            media = ceil(mean(puntuaciones_l))
        else:
            media = 0

        return media
    
    def __str__(self):
        return self.usuario.username
    
    class Meta:
        ordering = ('pk', )

class Compra(models.Model):
    comprador = models.ForeignKey(Perfil, related_name='comprador', on_delete=models.SET_NULL, null=True)
    vendedor = models.ForeignKey(Perfil, related_name='vendedor', on_delete=models.SET_NULL, null=True)
    nombre = models.TextField(verbose_name='Nombre de la impresión', blank=True)
    descripcion = models.TextField(verbose_name='Descripción de la impresión', blank=True)
    precio = models.FloatField(verbose_name='Precio de la impresión', null=True)
    direccion = models.ForeignKey('DirecPerfil', on_delete=models.SET_NULL, null=True)
    tamaño = models.TextField(verbose_name='Tamaño', null=True)
    material = models.TextField(verbose_name='Material', null=True)
    fecha_compra = models.DateField(verbose_name="Fecha de compra")
    pagado = models.BooleanField(verbose_name='Pagado por administrador?')

    def __str__(self):
        return self.nombre + str(self.fecha_compra)

    class Meta:
        ordering = ('pk', 'fecha_compra', )

class Presupuesto(models.Model):
    interesado = models.ForeignKey(Perfil, related_name='Interesado', on_delete=models.SET_NULL, null=True)
    vendedor = models.ForeignKey(Perfil, related_name='Vendedor', on_delete=models.SET_NULL, null=True)
    peticion = models.TextField(verbose_name='Peticion')
    descripcion = models.TextField(verbose_name='Descripcion')
    precio = models.FloatField(verbose_name='Precio', null=True)
    notas = models.TextField(verbose_name='Notas', null=True)
    tamaño = models.TextField(verbose_name='Tamaño', null=True)
    material = models.TextField(verbose_name='Material', null=True)
    fecha_envio = models.DateField(verbose_name="Fecha de envio", null=True)
    resp_interesado = models.BooleanField(verbose_name='Respuesta del Interesado', null=True)
    resp_vendedor = models.BooleanField(verbose_name='Respuesta del Vendedor', null=True)

    def __str__(self):
        return self.peticion
    
    class Meta:
        ordering = ('pk', )

class Opinion(models.Model):
    compra = models.ForeignKey(Compra, related_name='Compra', on_delete=models.CASCADE, null=False)
    puntuador = models.ForeignKey(Perfil, related_name='Puntuador', on_delete=models.CASCADE, null=False)
    nota = models.IntegerField(verbose_name='Nota', validators=[MinValueValidator(1), MaxValueValidator(5)])
    opinion = models.TextField(verbose_name='Opinion')

    def __str__(self):
        return str(self.nota)
    
    class Meta:
        ordering = ('pk', )