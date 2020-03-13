from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Impresion, Perfil, Imagen, Compra,Categoria
from main.forms import ImpresionForm, CargarImagenForm

def error(request):
    return render(request, 'impresiones/paginaError.html')

def listarImpresiones(request):

    try:
        impresiones = Impresion.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'impresiones/listarImpresiones.html', {'impresiones':impresiones,'categorias':categorias})
    except:
        return redirect('error_url')

def index(request):
    return render(request, 'index.html',)

