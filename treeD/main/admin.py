from django.contrib import admin
from main.models import Impresion, Perfil, Compra, ImgImpresion, ImgCompra, ImgPrueba, Categoria, DirecPerfil, Presupuesto

# Register your models here.
admin.site.register(Impresion)
admin.site.register(Compra)
admin.site.register(ImgImpresion)
admin.site.register(ImgCompra)
admin.site.register(ImgPrueba)
admin.site.register(Categoria)
admin.site.register(Presupuesto)
