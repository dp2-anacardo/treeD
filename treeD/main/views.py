from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Impresion, Perfil, Compra
from datetime import date
from main.forms import BuscadorForm

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


def usuarioLogueado(request):

    idUser=request.user.id
    userActual = get_object_or_404(User, pk = idUser)
    usuarioActual = Perfil.objects.get(usuario = userActual)
    return usuarioActual


def comprarImpresion3D(request, idImpresion):
    try:
        impresion = Impresion.objects.get(idImpresion=idImpresion)
        perfil = usuarioLogueado(request)
        idPerfil = perfil.idPerfil
        
        assert impresion.publicador != perfil

        compras = list(Compra.objects.all().filter(idPerfil = idPerfil))
        fechaActual = date.today()

        compra = Compra(idPerfil=perfil, idImpresion=impresion, fechaDeCompra=fechaActual)
        compra.save()

        compras.append(compra)

        impresiones=[]
        diccionario={}

        for c in compras:
            impresionCompra= Impresion.objects.get(idImpresion = c.idImpresion.idImpresion)
            impresiones.append(impresionCompra)


        for c in compras:
            for i in impresiones:
                if c.idImpresion.idImpresion == i.idImpresion:
                    diccionario[c]=i
                    impresiones.remove(i)
                    break

        return render(request, 'impresiones/misCompras.html', {'diccionario':diccionario})
    except:
        return redirect('error_url')


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

