from django.contrib import admin
from .models import Imagen, Impresion, Perfil, Compra, Categoria

# Register your models here.
admin.site.register(Imagen)
admin.site.register(Impresion)
admin.site.register(Perfil)
admin.site.register(Compra)
admin.site.register(Categoria)