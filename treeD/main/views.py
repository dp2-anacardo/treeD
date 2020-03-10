from django.shortcuts import render
from django.contrib.auth.models import User
from main.models import Impresion, Perfil, Imagen, Compra

# Create your views here.

def listarComprasImpresiones(request):

    usuario = request.user
    perfil = Perfil.objects.all().filter(usuario = usuario)
    comprasRealizadas = perfil.impresionesCompradas
    return render(request, 'impresiones/listarCompras.html', {'impresiones':comprasRealizadas})