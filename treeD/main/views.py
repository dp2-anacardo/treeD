from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Impresion, Perfil, Compra,Categoria
from django.shortcuts import render
from main.forms import BuscadorForm

# Create your views here.

def usuarioLogueado(request):

    idUser=request.user.id
    userActual = get_object_or_404(User, pk = idUser)
    usuarioActual = Perfil.objects.get(usuario = userActual)
    return usuarioActual

def error(request):
    return render(request, 'impresiones/paginaError.html')

def listarComprasImpresiones(request):

    try:
        usuario = usuarioLogueado(request)
        compras = list(Compra.objects.all().filter(comprador = usuario))
        return render(request, 'impresiones/listarCompras.html', {'compras':compras})
    except:
        return redirect('error_url')

def listarImpresiones(request):

    try:
        form = BuscadorForm(request.POST)
        impresiones = Impresion.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'impresiones/listarImpresiones.html', {'impresiones':impresiones,'categorias':categorias,'form':form})
    except EmptyResultSet:
        return redirect('error_url')

def index(request):
    return render(request, 'index.html',)

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

