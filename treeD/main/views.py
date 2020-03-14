from django.shortcuts import render, redirect
from main.models import Impresion,Categoria

def error(request):
    return render(request, 'impresiones/paginaError.html')

def listarImpresiones(request):

    try:
        impresiones = Impresion.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'impresiones/listarImpresiones.html', {'impresiones':impresiones,'categorias':categorias})
    except EmptyResultSet:
        return redirect('error_url')

def index(request):
    return render(request, 'index.html',)

