from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Impresion, Perfil, Compra

# Create your views here.

def usuarioLogueado(request):

    idUser=request.user.id
    userActual = get_object_or_404(User, pk = idUser)
    usuarioActual = Perfil.objects.get(usuario = userActual)
    return usuarioActual

def listarComprasImpresiones(request):

    try:
        usuario = usuarioLogueado(request)
        idUsuario = usuario.idPerfil
        compras = list(Compra.objects.all().filter(idPerfil = idUsuario))
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

        return render(request, 'impresiones/listarCompras.html', {'diccionario':diccionario})
    except:
        return redirect('error_url')


