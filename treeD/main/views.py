from functools import reduce
import operator

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from main.forms import BuscadorForm
from main.models import Impresion

# Create your views here.
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
                query = query.objects.filter(nombre__icontains=nombre)
            if categorias:
                query = query.filter(reduce(
                    operator.and_, (Q(categorias__contains=c) for c in categorias)))
            if precio_min is not None:
                query = query.filter(precio__gt=precio_min)
            if precio_max is not None:
                query = query.filter(precio__lt=precio_max)

    else:
        form = BuscadorForm()

    return render(request, "list.html", {"form": form, "query": query})
