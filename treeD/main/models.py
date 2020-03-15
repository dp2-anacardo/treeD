from django.db import models
from django.contrib.auth.models import User


class Imagen(models.Model):
    idImagen = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='imagenes',verbose_name='Imagen')
    impresion = models.ForeignKey('Impresion', on_delete=models.CASCADE)
    compra = models.ForeignKey('Compra', on_delete=models.SET_NULL, null= True)

    def __str__(self):
        return str(self.idImagen)

    class Meta:
        ordering = ('idImagen',)

class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    categoria = models.TextField(verbose_name='Categoría')

    def __str__(self):
        return self.categoria
    
    class Meta:
        ordering = ('idCategoria', )

class Impresion(models.Model):
    idImpresion = models.AutoField(primary_key=True)
    nombre = models.TextField(verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción') 
    precio = models.FloatField(verbose_name='Precio')
    vendedor = models.ForeignKey('Perfil', on_delete=models.CASCADE, null = True)
    categorias = models.ManyToManyField('Categoria')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('idImpresion', )    


class Perfil(models.Model):
    idPerfil = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User,on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.usuario.username
    
    class Meta:
        ordering = ('idPerfil', )
        

class Compra(models.Model):
    idCompra = models.AutoField(primary_key=True)
    comprador = models.ForeignKey(Perfil, related_name='comprador', on_delete=models.SET_NULL, null = True)
    vendedor = models.ForeignKey(Perfil, related_name='vendedor', on_delete=models.SET_NULL, null = True)
    nombreImpresion = models.TextField(verbose_name='Nombre de la impresión', blank=True)
    descripcionImpresion = models.TextField(verbose_name='Descripción de la impresión', blank= True)
    precioImpresion = models.FloatField(verbose_name='Precio de la impresión', null = True)
    fechaDeCompra = models.DateField(verbose_name="Fecha de compra")

    def __str__(self):
        return str(self.fechaDeCompra)

    class Meta:
        ordering = ('idCompra', 'fechaDeCompra', )



