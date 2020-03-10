from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Impresion, Perfil, Imagen, Compra,Categoria
from main.forms import ImpresionForm, CargarImagenForm

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
def crearImpresionUnificada(request):

    if request.method == "POST":
        formImpresion = ImpresionForm(request.POST)
        formImagen1 = CargarImagenForm(request.POST, request.FILES)
        formImagen2 = CargarImagenForm(request.POST, request.FILES)
        formImagen3= CargarImagenForm(request.POST, request.FILES)
        formImagen4=CargarImagenForm(request.POST, request.FILES)
        if formImpresion.is_valid() and formImagen1.is_valid():
            imagen1 = formImagen1.save(commit=False)
            imagen2 = formImagen2.save(commit=False)
            imagen3= formImagen3.save(commit=False)
            imagen4= formImagen4.save(commit=False)
            imagen1.impresion= formImpresion.save()
            imagen2.impresion=formImpresion.save()
            imagen3.impresion=formImpresion.save()
            imagen4.impresion=formImpresion.save()
            imagen1.save() 
            imagen2.save()
            imagen3.save()
            imagen4.save()
            return redirect('index')
    else:
        formImpresion = ImpresionForm()
        formImagen1 = CargarImagenForm()
        formImagen2=CargarImagenForm()
        formImagen3= CargarImagenForm()
        formImagen4=CargarImagenForm()
    return render(request, 'impresiones/crearImpresion.html',{'formulario1':formImpresion, 'formulario2':formImagen1,
     'formulario3':formImagen2, 'formulario4':formImagen3,'formulario5':formImagen4})

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

def error(request):
    return render(request, 'impresiones/paginaError.html')

def listarImpresiones(request):

    try:
        usuario = usuarioLogueado(request)
        impresiones = Impresion.objects.all()
        return render(request, 'impresiones/listarImpresiones.html', {'impresiones':impresiones})
    except:
        return redirect('error_url')

def index(request):
    return render(request, 'index.html',)

