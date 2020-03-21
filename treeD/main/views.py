""" Vistas del sistema
"""
from django.core.exceptions import EmptyResultSet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Impresion, Perfil, Compra, Categoria, ImgImpresion, ImgCompra
from main.forms import ImpresionForm, CargarImagenForm, BuscadorForm
from datetime import date
from django.urls import reverse
from paypal.standard.forms import PayPalEncryptedPaymentsForm, PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def usuario_logueado(request):

    id_user = request.user.id
    user_actual = get_object_or_404(User, pk=id_user)
    usuario_actual = Perfil.objects.get(usuario=user_actual)
    return usuario_actual


def error(request):
    return render(request, 'impresiones/paginaError.html')

def listar_compras_impresiones(request):

    try:
        usuario = usuario_logueado(request)
        compras = list(Compra.objects.all().filter(comprador=usuario))
        return render(request, 'impresiones/listarCompras.html', {'compras': compras})
    except:
        return redirect('error_url')

def listar_impresiones(request):

    try:
        form = BuscadorForm(request.POST)
        impresiones = Impresion.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'impresiones/listarImpresiones.html', {
            'impresiones':impresiones,
            'categorias':categorias,
            'form':form
        })
    except:
        return redirect('error_url')

def home(request):
    return render(request, 'impresiones/index.html')

@csrf_exempt
def mostrar_impresion(request, pk):
    
    try:
        impresion = Impresion.objects.get(pk=pk)
        precio = impresion.precio + 1
        idImpresion = str(pk)

        paypal_dict = {
        "business": "treeD@business.example.com",
        "amount": str(precio),
        "item_name": impresion.nombre,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('comprarImpresion_url' , args=[idImpresion])),
        "cancel_return": request.build_absolute_uri(reverse('mostrarImpresion_url' , args=[idImpresion])),
        }

        if settings.DEBUG == False:
            form = PayPalEncryptedPaymentsForm(initial=paypal_dict)
        else:
            form = PayPalPaymentsForm(initial=paypal_dict)

        comprar = True
        user = None
        try:
            user = usuario_logueado(request)
        except:
            pass
        if user is None or user == impresion.vendedor:
            comprar = False
        categorias = impresion.categorias.all()
        imagenes_impresion = ImgImpresion.objects.filter(impresion=impresion)
        return render(request, 'impresiones/mostrarImpresion.html', {
            'impresion': impresion,
            'imagenes': imagenes_impresion,
            'categorias': categorias,
            'comprar': comprar,
            'form': form
        })
    except:
        return redirect('error_url')

def crear_impresion(request):

    try:
        numero_imagenes = 4
        if request.method == "POST":
            form_impresion = ImpresionForm(request.POST)
            form_imagen = CargarImagenForm(request.POST, request.FILES)
            files = request.FILES.getlist('imagen')
            if form_impresion.is_valid() and form_imagen.is_valid():
                categorias = form_impresion.cleaned_data.get("categorias")
                print(categorias)
                if not categorias:
                    categorias = Categoria.objects.filter(categoria='OTRAS COSAS')
                impresion = form_impresion.save(commit=False)
                impresion.vendedor = usuario_logueado(request)
                impresion.save()
                impresion.categorias.set(categorias)
                contador = 1
                for i in files:
                    if contador <= numero_imagenes:
                        imagen = ImgImpresion(imagen=i, impresion=impresion)
                        imagen.save()
                    contador = contador + 1
                return redirect('/misPublicaciones')
        else:
            form_impresion = ImpresionForm()
            form_imagen = CargarImagenForm(request.FILES)
        return render(request, 'impresiones/crearImpresion.html', {
            'formulario1':form_impresion,
            'formulario_imagen':form_imagen
        })
    except:
        return redirect('error_url')

def eliminar_impresion(request, pk):

    try:
        impresion = Impresion.objects.get(pk=pk)
        vendedor_impresion = impresion.vendedor
        usuario = usuario_logueado(request)
        if vendedor_impresion != usuario:
            return redirect('error_url')
        imagenes_impresion = ImgImpresion.objects.filter(impresion=impresion)
        imagenes_impresion.delete()
        impresion.delete()
        return redirect('/misPublicaciones')
    except:
        return redirect('error_url')

def editar_impresion(request, pk):

    try:
        impresion = Impresion.objects.get(pk=pk)
        vendedor_impresion = impresion.vendedor
        imagenes_impresion = ImgImpresion.objects.filter(impresion=impresion)
        usuario = usuario_logueado(request)
        if vendedor_impresion != usuario:
            return redirect('error_url')
        if request.method == 'GET':
            form_impresion = ImpresionForm(instance=impresion)
            return render(request, 'impresiones/editarImpresion.html', {
                'formulario1': form_impresion,
                'imagenes': imagenes_impresion,
                'pk': pk
            })
        else:
            form_impresion = ImpresionForm(request.POST, instance=impresion)
            if form_impresion.is_valid():
                form_impresion.save()
                return redirect('/misPublicaciones')
    except:
        return redirect('error_url')
    
def index(request):
    form = BuscadorForm(request.POST)
    return render(request, 'index.html', {'form': form})

def listar_impresiones_publicadas(request):
    """
    Funcion que lista las impresiones publicadas por un vendedor
    """
    if request.user.is_authenticated:
        perfil_user = Perfil.objects.get(usuario=request.user)
        query = Impresion.objects.filter(vendedor=perfil_user)
        return render(request, "misPublicaciones.html", {"query": query})

    return render(request, 'index.html')

@csrf_exempt
def comprar_impresion_3d(request, pk):

    try:
        impresion = Impresion.objects.get(pk=pk)
        comprador = usuario_logueado(request)
        
        assert impresion.vendedor != comprador
        compras = list(Compra.objects.filter(comprador=comprador))
        fecha_actual = date.today()

        imagenes = list(ImgImpresion.objects.filter(impresion=impresion))

        compra = Compra(
            comprador=comprador,
            vendedor=impresion.vendedor,
            nombre_impresion=impresion.nombre,
            desc_impresion=impresion.descripcion,
            precio_impresion=impresion.precio,
            fecha_compra=fecha_actual
        )
        compra.save()

        for img in imagenes:
            imagen = ImgCompra(imagen=img.imagen, compra=compra)
            imagen.save()

        compras.append(compra)

        return render(request, 'impresiones/listarCompras.html', {'compras': compras})
        
    except:
        return redirect('error_url')


def buscador_impresiones_3d(request):

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
                query = query.filter(precio__gte=precio_min)
            if precio_max is not None:
                query = query.filter(precio__lte=precio_max)

    else:
        form = BuscadorForm()

    return render(request, "impresiones/listarImpresiones.html", {"form": form, "impresiones": query})

def listar_ventas_realizadas(request):
   
    if request.user.is_authenticated:
        perfil_user = Perfil.objects.get(usuario=request.user)
        query = Compra.objects.filter(vendedor=perfil_user)
        return render(request, "impresiones/listarVentas.html", {"query": query})

    return render(request, 'index.html') 