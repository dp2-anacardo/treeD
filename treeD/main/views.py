from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from main.forms import BuscadorForm
from main.models import Impresion, Perfil
from django.shortcuts import render, redirect
from main.models import Impresion,Categoria,Imagen
from main.forms import ImpresionForm, CargarImagenForm

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
                categorias = formImpresion.cleaned_data.get("categorias")
                impresion = formImpresion.save(commit=False)
                impresion.vendedor = usuarioLogueado(request)
                impresion.save()
                impresion.categorias.set(categorias)
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
        vendedorImpresion= impresion.vendedor
        usuario = usuarioLogueado(request)
        if vendedorImpresion != usuario:
            return redirect('error_url') 
        imagenesImpresion=Imagen.objects.all().filter(impresion=impresion)
        imagenesImpresion.delete()
        impresion.delete()
        return redirect('index')
    except:
        return redirect('error_url')

def editarImpresion(request, idImpresion):

    try:
        impresion= Impresion.objects.get(idImpresion = idImpresion)
        vendedorImpresion = impresion.vendedor
        imagenesImpresion = Imagen.objects.all().filter(impresion=impresion)
        usuario = usuarioLogueado(request)
        if vendedorImpresion != usuario:
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

