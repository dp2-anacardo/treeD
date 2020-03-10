from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Impresion, Perfil
from datetime import date

# Create your views here.

def index(request):
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
        compras = Compra.objects.all().filter(idPerfil=idPerfil)
        fechaActual = date.today()

        compra = Compra(idPerfil=idPerfil, idImpresion=impresion.idImpresion, fechaDeCompra=fechaActual)
        compra.save()

        compras.append(compra)

        for c in compras:
            impresiones= []
            impresionCompra= Impresion.objects.all().filter(idImpresion=c.idImpresion)
            impresiones.append(impresionCompra)

        diccionario = {}

        for c in compras:
            for i in impresiones:
                if c.idImpresion == i.idImpresion:
                    diccionario[c]=i
                    impresiones.remove(i)
                    break

        return render(request, 'impresiones/misCompras.html', {'diccionario':diccionario})
    except:
        return redirect('error_url')