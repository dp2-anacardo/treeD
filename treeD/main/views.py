from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Impresion, Perfil, Imagen, Compra
from main.forms import ImpresionForm, CargarImagenForm
from django.forms import modelformset_factory

#Metodo para obtener el usuario actualmente logueado
def usuarioLogueado(request):

    idUser=request.user.id
    userActual = get_object_or_404(User, pk = idUser)
    usuarioActual = Perfil.objects.get(usuario = userActual)
    return usuarioActual

def home(request):
    return render(request, 'impresiones/index.html')

def error(request):
    return render(request, 'impresiones/paginaError.html')

def mostrarImpresion(request, idImpresion):
    
    try:
        impresion = Impresion.objects.get(idImpresion=idImpresion)
        imagenesTotales= Imagen.objects.all()
        categorias = impresion.categorias.all()
        imagenesImpresion = imagenesTotales.filter(impresion = impresion)
        return render(request, 'impresiones/mostrarImpresion.html', {'impresion':impresion, 'imagenes':imagenesImpresion, 'categorias':categorias})
    except:
        return redirect('error_url')
    

def crearImpresion(request):

    try:
        numeroImagenes = 4
        if request.method == "POST":
            formImpresion = ImpresionForm(request.POST)
            formImagen= CargarImagenForm(request.POST, request.FILES)
            files = request.FILES.getlist('imagen')
            if formImpresion.is_valid() and formImagen.is_valid():
                impresion = formImpresion.save(commit=False)
                impresion.publicador = usuarioLogueado(request)
                impresion.save()
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
    except:
        return redirect('error_url')

def eliminarImpresion(request, idImpresion):

    try:
        impresion= Impresion.objects.get(idImpresion = idImpresion)
        publicadorImpresion= impresion.publicador
        usuario = usuarioLogueado(request)
        if publicadorImpresion != usuario:
            return redirect('error_url') 
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
    except:
        return redirect('error_url')

def editarImpresion(request, idImpresion):

    try:
        impresion= Impresion.objects.get(idImpresion = idImpresion)
        publicadorImpresion = impresion.publicador
        imagenesImpresion = Imagen.objects.all().filter(impresion=impresion)
        usuario = usuarioLogueado(request)
        if publicadorImpresion != usuario:
            return redirect('error_url') 
        if request.method == 'GET':
            formImpresion= ImpresionForm(instance= impresion)
            return render(request, 'impresiones/editarImpresion.html',{'formulario1':formImpresion, 'imagenes':imagenesImpresion, 'id':idImpresion})
        else:
            formImpresion = ImpresionForm(request.POST, instance=impresion)
            if formImpresion.is_valid():
                formImpresion.save()
                return redirect('index')
    except:
        return redirect('error_url')

def eliminarImagen(request, idImagen):

    try:
        img = Imagen.objects.get(idImagen = idImagen)
        impresion = img.impresion
        publicadorImpresion = impresion.publicador
        idImpresion = impresion.idImpresion
        usuario = usuarioLogueado(request)
        if publicadorImpresion != usuario:
            return redirect('error_url')
        img.delete()

        impresion= Impresion.objects.get(idImpresion = idImpresion)
        imagenesImpresion = Imagen.objects.all().filter(impresion=impresion)
        formImpresion= ImpresionForm(instance= impresion)
        return render(request, 'impresiones/editarImpresion.html',{'formulario1':formImpresion,'imagenes':imagenesImpresion})
    except:
        return redirect('error_url')

def añadirImagen(request, idImpresion):

    try:
        numeroImagenes = 4
        impresion = Impresion.objects.get(idImpresion = idImpresion)
        publicadorImpresion = impresion.publicador
        imagenesImpresion = Imagen.objects.all().filter(impresion=impresion)
        formImpresion= ImpresionForm(instance= impresion)
        numeroImagenesImpresiones = len(imagenesImpresion)

        usuario = usuarioLogueado(request)
        if publicadorImpresion != usuario:
            return redirect('error_url')

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
    except:
        return redirect('error_url')

    
def index(request):
    return render(request, 'index.html',)

