from django.shortcuts import render, redirect, get_object_or_404
from main.models import Impresion, Usuario
from django.contrib.auth.models import User
from main.forms import ImpresionForm

#Metodo para obtener el usuario actualmente logueado
def usuarioLogueado():

    idUser=request.user.id
    userActual = get_object_or_404(User, pk = idUser)
    usuarioActual = Usuario.objects.get(usuario = usuarioActual)
    return usuarioActual

def mostrarImpresion(request, idImpresion):
    
    #Obtener la impresion seleccionada
    impresion = Impresion.objects.get(idImpresion=idImpresion)
    return render(request, 'carpeta/archivo.html', {'impresion':impresion})

def mostrarTodasMisImpresiones(request):

    #Obtener todas las impresiones
    impresiones=Impresion.objects.all
    #Filtrar todas las impresiones por el usuario logueado en el sistema
    usuarioActual = usuarioLogueado()
    impresionesUsuario = impresiones.filter(vendedor__usuario = usuarioActual)
    return render(request, 'carpeta/archivo.html',{'impresionesUsuario': impresionesUsuario})

def crearImpresion(request):

    #Se crea la impresion mediante un formulario en forms.py llamado ImpresionForm()
    if request.method == 'POST':
        formulario = ImpresionForm(request.POST)
        if formulario.is_valid():
            #Se hace el commit=False para simular el save en la base de datos y añadir datos extra 
            # y por ultimo se vuelve ha hacer el save en la base de datos
            post=formulario.save(commit=False)
            post.vendedor = usuarioLogueado()
            post.save()
            return redirect('nombrePaginaDestino')
        else:
            formulario = ImpresionForm()
    return render(request, 'carpeta/archivo.html',{'form':formulario})

def editarImpresion(request, idImpresion):

    impresion = Impresion.objects.get(idImpresion = idImpresion)
    #Si la impresion no pertenece al usuario logueado no la puede editar
    if impresion.vendedor == usuarioLogueado():
        if request.method == 'GET':
            formulario = ImpresionForm(instance = impresion)
        else:
            formulario = ImpresionForm(request.POST, instance=impresion)
            if formulario.is_valid:
                formulario.save()
            return redirect('nombrePaginaDestino')
        return render(request, 'carpeta/archivo.html',{'form':formulario})
    else:
        return redirect('paginaError.html')


def eliminarImpresion(request, idImpresion):

    #Obetener la impresion seleccionada y vendedor de la impresion
    impresion = Impresion.objects.get(idImpresion= idImpresion)
    vendedor= impresion.vendedor
    #Comprobación de que la persona que elimina la impresion es su propio vendedor
    if vendedor.usuario.username == request.user.username:
        # Primero se elimina la impresion de la lista de compra de todos sus compradores y despues 
        # se elimina la impresion de la base de datos
        usuarios = Usuario.objects.all()
        for u in usuarios:
            if impresion in u.impresionesCompradas:
                u.impresionesCompradas.remove(impresion)
        impresion.delete()
        return render(request, 'carpeta/archivo.html',{})
    else:
        #Se envia a la vista de error con su mensaje correspondiente
        mensajeError='Ha habido un error inesperado'
        return render(request, 'paginaError.html',{'mensajeError':mensajeError})