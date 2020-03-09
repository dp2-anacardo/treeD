from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Impresion, Perfil, Imagen, Compra
from main.forms import ImpresionForm, CargarImagenForm
from django.forms import modelformset_factory

#Metodo para obtener el usuario actualmente logueado
def usuarioLogueado(request):

    idUser=request.user.id
    userActual = get_object_or_404(User, pk = idUser)
    usuarioActual = Perfil.objects.get(usuario = usuarioActual)
    return usuarioActual

def home(request):
    return render(request, 'impresiones/index.html')

def mostrarImpresion(request, idImpresion):
    
    impresion = Impresion.objects.get(idImpresion=idImpresion)
    imagenesTotales= Imagen.objects.all()
    imagenesImpresion = imagenesTotales.filter(impresion = impresion)
    return render(request, 'impresiones/mostrarImpresion.html', {'impresion':impresion, 'imagenes':imagenesImpresion})

#Falta añadir a mano el publicador que seria el usuario logueado
def crearImpresion(request):

    numeroImagenes = 4
    if request.method == "POST":
        formImpresion = ImpresionForm(request.POST)
        formImagen= CargarImagenForm(request.POST, request.FILES)
        files = request.FILES.getlist('imagen')
        if formImpresion.is_valid() and formImagen.is_valid():
            impresion = formImpresion.save()
            contador = 1
            for i in files:
                if contador <= numeroImagenes:
                    imagen = Imagen(imagen=i, impresion=impresion)
                    imagen.save()
                contador = contador + 1
            return redirect('index')
    else:
        formImpresion = ImpresionForm()
        formImagen=CargarImagenForm(request.FILES)
    return render(request, 'impresiones/crearImpresion.html',{'formulario1':formImpresion, 'formularioImagen':formImagen})

#Falta hacer comprobacion de que solo el publicador de la impresion pueda eliminarla
def eliminarImpresion(request, idImpresion):

    impresion= Impresion.objects.get(idImpresion = idImpresion)
    publicadorImpresion= impresion.publicador
    imagenesImpresion=Imagen.objects.all().filter(impresion=impresion)
    compras= Compra.objects.all().filter(idImpresion = idImpresion)
    if len(compras)>0:
        impresion.publicador=None
        impresion.save()
        return redirect('index')
    else:
        imagenesImpresion.delete()
        impresion.delete()
    return redirect('index')

#Falta hacer comprobacion de que solo el publicador de la impresion pueda editarla
def editarImpresion(request, idImpresion):

    impresion= Impresion.objects.get(idImpresion = idImpresion)
    imagenesImpresion = Imagen.objects.all().filter(impresion=impresion)

    if request.method == 'GET':
        formImpresion= ImpresionForm(instance= impresion)
        return render(request, 'impresiones/editarImpresion.html',{'formulario1':formImpresion, 'imagenes':imagenesImpresion, 'id':idImpresion})
    else:
        formImpresion = ImpresionForm(request.POST, instance=impresion)
        if formImpresion.is_valid():
            formImpresion.save()
            return redirect('index')

def eliminarImagen(request, idImagen):

    img = Imagen.objects.get(idImagen = idImagen)
    idImpresion = img.impresion.idImpresion
    img.delete()

    impresion= Impresion.objects.get(idImpresion = idImpresion)
    imagenesImpresion = Imagen.objects.all().filter(impresion=impresion)
    formImpresion= ImpresionForm(instance= impresion)
    return render(request, 'impresiones/editarImpresion.html',{'formulario1':formImpresion,'imagenes':imagenesImpresion})

def añadirImagen(request, idImpresion):

    numeroImagenes = 4
    impresion = Impresion.objects.get(idImpresion = idImpresion)
    imagenesImpresion = Imagen.objects.all().filter(impresion=impresion)
    formImpresion= ImpresionForm(instance= impresion)
    numeroImagenesImpresiones = len(imagenesImpresion)
    print(numeroImagenesImpresiones)

    if request.method == "POST":
        formImagen= CargarImagenForm(request.POST, request.FILES)
        files = request.FILES.getlist('imagen')
        if formImagen.is_valid():
            contador = 1
            for i in files:
                if contador + numeroImagenesImpresiones <= numeroImagenes:
                    imagen = Imagen(imagen=i, impresion=impresion)
                    imagen.save()
                contador = contador + 1
            return redirect('index')
    else:
        formImagen=CargarImagenForm(request.FILES)
    return render(request, 'impresiones/añadirImagen.html',{'formularioImagen':formImagen})

    

