""" Vistas del sistema
"""
from main.forms import BuscadorForm
from django.shortcuts import render, redirect
from main.models import Impresion, Categoria, Perfil
from django.core.exceptions import EmptyResultSet

def error(request):
    return render(request, 'impresiones/paginaError.html')

def listarImpresiones(request):

    try:
        form = BuscadorForm(request.POST)
        impresiones = Impresion.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'impresiones/listarImpresiones.html', {'impresiones':impresiones,'categorias':categorias,'form':form})
    except EmptyResultSet:
        return redirect('error_url')

def index(request):
    """
    Funcion que carga la pagina principal
    """
    return render(request, 'index.html',)

def listar_impresiones_publicadas(request):
    """
    Funcion que lista las impresiones publicadas por un vendedor
    """
    if request.user.is_authenticated:
        perfil_user = Perfil.objects.get(usuario=request.user)
        query = Impresion.objects.filter(publicador=perfil_user)
        return render(request, "list2.html", {"query": query})

    return render(request, 'index.html')

def buscador_impresiones_3d(request):
    """
    Funcion que busca impresiones 3D que cumplen una serie de parametros
    """
    query = Impresion.objects.all()

    if request.method == "POST":
        form = BuscadorForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get("nombre")
            categorias = form.cleaned_data.get("categorias")
            precio_min = form.cleaned_data.get("precio_min")
            precio_max = form.cleaned_data.get("precio_max")

            if nombre != '':
                query = query.filter(nombre__icontains=nombre)
            if categorias:
                for id_ in categorias:
                    query = query.filter(categorias__in=[id_]).distinct()
            if precio_min is not None:
                query = query.filter(precio__gt=precio_min)
            if precio_max is not None:
                query = query.filter(precio__lt=precio_max)

    else:
        form = BuscadorForm()

    return render(request, "impresiones/listarImpresiones.html", {"form": form, "impresiones": query})
