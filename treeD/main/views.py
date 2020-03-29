""" Vistas del sistema
"""
from django.core.exceptions import EmptyResultSet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse
from paypal.standard.forms import PayPalEncryptedPaymentsForm, PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from main.forms import *
from main.models import Impresion, Perfil, Compra, Categoria, ImgImpresion, ImgCompra, DirecPerfil
from datetime import date
from django.contrib.auth import login, authenticate

@login_required(login_url="/login/")
def editar_usuario_logueado(request):
    usuario = User.objects.get(pk=request.user.id)
    perfil = Perfil.objects.get(usuario=usuario)

    if request.method == "POST":
        form_1 = EditarUsernameForm(data=request.POST, instance=usuario)
        form_2 = EditarPerfilForm(data=request.POST, files=request.FILES, instance=perfil)
        if form_1.is_valid() and form_2.is_valid():
            form_1.save()
            form_2.save()
            #TODO: Redirigir a show de perfil cuando este hecho
            return redirect("/perfil/"+str(usuario.perfil.id))

        else:
            return render(request, "editarPerfil.html", {
                "form_1": form_1,
                "form_2": form_2,
            })

    else:
        form_1 = EditarUsernameForm(instance=usuario)
        form_2 = EditarPerfilForm(instance=perfil)
        return render(request, "editarPerfil.html", {
            "form_1": form_1,
            "form_2": form_2
        })

@login_required(login_url="/login/")
def editar_pw_usuario_logueado(request):
    usuario = User.objects.get(pk=request.user.id)

    if request.method == "POST":
        form = EditarPasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            usuario.set_password(password)
            usuario.save()
            #TODO: Redirigir a show de perfil cuando este hecho
            return redirect("/")

        else:
            return render(request, "editarPassword.html", {
                "form": form
            })

    else:
        form = EditarPasswordForm()
        return render(request, "editarPassword.html", {
            "form": form
        })

@login_required(login_url="/login/")
def mostrar_direcciones_usuario_logueado(request):
    usuario = User.objects.get(pk=request.user.id)
    perfil = Perfil.objects.get(usuario=usuario)
    direcciones = DirecPerfil.objects.filter(perfil=perfil)
    form = AñadirDirecPerfilForm()
    return render(request, "mostrarDirecciones.html", {
        "direcciones": direcciones,
        "form": form
    })

@login_required(login_url="/login/")
def añadir_direccion_usuario_logueado(request):
    usuario = User.objects.get(pk=request.user.id)
    perfil = Perfil.objects.get(usuario=usuario)

    if request.method == "POST":
        form = AñadirDirecPerfilForm(request.POST)
        if form.is_valid():
            direc = form.cleaned_data.get("direccion")
            dp = DirecPerfil(direccion=direc, perfil=perfil)
            dp.save()
            #TODO: Redirigir a show de perfil cuando este hecho
            return redirect("/mostrarDirecciones")

        else:
            return redirect("/mostrarDirecciones")

    else:
        return redirect("/mostrarDirecciones")

@login_required(login_url="/login/")
def eliminar_direccion_usuario_logueado(request, pk):
    usuario = User.objects.get(pk=request.user.id)
    perfil = Perfil.objects.get(usuario=usuario)

    try:
        direc = DirecPerfil.objects.get(pk=pk)
        if direc.perfil != perfil:
            return redirect('error_url')
        direc.delete()
        return redirect('/mostrarDirecciones')
    except:
        return redirect('error_url')

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
        impresiones_no_afiliados = list(Impresion.objects.all().filter(vendedor__es_afiliado=False))
        impresiones_afiliados = list(Impresion.objects.all().filter(vendedor__es_afiliado=True))
        impresiones_afiliados.extend(impresiones_no_afiliados)
        categorias = Categoria.objects.all()
        return render(request, 'impresiones/listarImpresiones.html', {
            'impresiones':impresiones_afiliados,
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
            'comprar': comprar
        })
    except:
        return redirect('error_url')

def crear_usuario(request):

    try:
        if request.user.is_authenticated == True:
            return redirect('error_url')
        
        if request.method == "POST":
            form_usuario = UserForm(request.POST)
            form_perfil = PerfilForm(request.POST)
            form_imagen = ImagenForm(request.POST, request.FILES)
            form_direccion = DirecPerfilForm(request.POST)
            if form_usuario.is_valid() and form_perfil.is_valid() and form_imagen.is_valid() and form_direccion.is_valid:
            
                usuario = form_usuario.save()
                perfil = form_perfil.save(commit = False)
                perfil.usuario = usuario
                if form_imagen.cleaned_data['imagen'] is not None:
                    imagen = request.FILES['imagen']
                    perfil.imagen = imagen
                perfil.es_afiliado = False
                perfil.save()
                
                direccion = form_direccion.save(commit = False)
                direccion.perfil = perfil
                direccion.save()

                username = form_usuario.cleaned_data['username']
                password = form_usuario.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
        
        else:
            form_usuario = UserForm()
            form_perfil = PerfilForm()
            form_direccion = DirecPerfilForm()
            form_imagen = ImagenForm(request.FILES)

        return render(request,'registration/register.html',{
            'form_usuario':form_usuario, 
            'form_perfil':form_perfil, 
            'form_direccion':form_direccion, 
            'form_imagen':form_imagen
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
def comprar_impresion_3d(request, pk, direccion):

    try:
        impresion = Impresion.objects.get(pk=pk)
        comprador = usuario_logueado(request)
        direc= DirecPerfil.objects.get(id = direccion)
        
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
            fecha_compra=fecha_actual,
            direccion = direc
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
            
            query = query.order_by('-vendedor__es_afiliado')
            
    else:
        form = BuscadorForm()

    return render(request, "impresiones/listarImpresiones.html", {"form": form, "impresiones": query})

def listar_ventas_realizadas(request):
   
    if request.user.is_authenticated:
        perfil_user = Perfil.objects.get(usuario=request.user)
        query = Compra.objects.filter(vendedor=perfil_user)
        return render(request, "impresiones/listarVentas.html", {"query": query})

    return render(request, 'index.html')

def buscar_usuarios(request):
    
    if request.user.is_authenticated:

        perfil_user = Perfil.objects.get(usuario=request.user)
        query = Perfil.objects.all().exclude(nombre = perfil_user.nombre)
        query = query.exclude(impresion__isnull=True)

        if request.method == "POST":
            form = BuscarUsuariosForm(request.POST)
            if form.is_valid():
                nombre = form.cleaned_data.get("nombre")
                query = query.filter(nombre__icontains=nombre)
                return render(request, "registration/listarUsuarios.html", {"form": form, "query": query})
        else:
            form = BuscarUsuariosForm()
            return render(request, "registration/listarUsuarios.html", {"form": form, "query": query})
    
    return render(request, 'index.html')

def detalles_compra(request, pk):

    try:
        impresion = Impresion.objects.get(pk=pk)
        comprador = usuario_logueado(request)

        if request.method == "POST":
            form = DireccionForm(request.POST)
            if form.is_valid():
                direccionSeleccionada = form.cleaned_data.get("direccion")
                direccion = DirecPerfil.objects.get(direccion=direccionSeleccionada)

                precio = impresion.precio + 1
                idImpresion = str(pk)

                paypal_dict = {
                    "business": "treeD@business.example.com",
                    "amount": str(precio),
                    "item_name": impresion.nombre,
                    "currency_code": "EUR",
                    "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                    "return": request.build_absolute_uri(reverse('comprarImpresion_url' , args=[idImpresion, direccion.id])),
                    "cancel_return": request.build_absolute_uri(reverse('mostrarImpresion_url' , args=[idImpresion])),
                }

                if settings.DEBUG == False:
                    formPago = PayPalEncryptedPaymentsForm(initial=paypal_dict)
                else:
                    formPago = PayPalPaymentsForm(initial=paypal_dict)

                vistaPaypal = True

                return render(request, "impresiones/facturarCompra.html", {"formPago": formPago, "perfil": comprador, 
                        'impresion':impresion, 'direccion':direccion, 'vistaPaypal': vistaPaypal})
        else:
            form = DireccionForm()
            form.fields['direccion'].queryset = DirecPerfil.objects.filter(perfil=comprador)
            
        vistaPaypal = False

        return render(request, "impresiones/facturarCompra.html", {"form": form, "perfil": comprador, 'impresion':impresion, 'vistaPaypal': vistaPaypal})

    except:
       return redirect('error_url')
    

def mostrar_perfil(request, pk):
    try:
        perfil = Perfil.objects.get(pk=pk)
        direcciones = DirecPerfil.objects.all().filter(perfil=perfil)

        impresiones = Impresion.objects.all().filter(vendedor=perfil)

        return render(request, 'perfil.html', {'perfil':perfil, 'direcciones':direcciones,
         'impresiones':impresiones})

    except:
        return redirect('error_url')
