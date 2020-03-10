from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Impresion, Perfil, Imagen, Compra

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
        compras = Compra.objects.all().filter(idPerfil = idUsuario)
        impresiones=[]
        for c in compras:
            idImpresion = c.idImpresion
            impresioncompra= Impresion.objects.get(idImpresion = idImpresion.idImpresion)
            impresiones.append(impresioncompra)
        return render(request, 'impresiones/listarCompras.html', {'compras':compras, 'impresiones':impresiones})
    except:
        return redirect('error_url')


