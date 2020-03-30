from django.core.exceptions import EmptyResultSet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import *
from main.forms import *
from datetime import date
from django.urls import reverse
from paypal.standard.forms import PayPalEncryptedPaymentsForm, PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import login, authenticate

@login_required(login_url="/login/")
def pedir_presupuesto(request, pk):
    try:
        interesado = User.objects.get(pk=request.user.id)
        p_interesado = Perfil.objects.get(usuario=interesado)
        p_vendedor = Perfil.objects.get(pk=pk)
        assert p_interesado != p_vendedor
        
        if request.method == "POST":
            form = PedirPresupuestoForm(data=request.POST)
            if form.is_valid():
                presupuesto = form.save(commit=False)
                presupuesto.vendedor = p_vendedor
                presupuesto.interesado = p_interesado
                presupuesto.save()
                return redirect("/presupuesto/enviados")
            else:
                return render(request, "pedirPresupuesto.html", {
                    "form": form,
                    'pk': pk
                })
        else:
            form = PedirPresupuestoForm()
            return render(request, "pedirPresupuesto.html", {
                    "form": form,
                    'pk': pk
            })
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def responder_presupuesto(request, pk):
    try:
        vendedor = User.objects.get(pk=request.user.id)
        p_vendedor = Perfil.objects.get(usuario=vendedor)
        presupuesto = Presupuesto.objects.get(pk=pk)
        assert presupuesto.vendedor.id == p_vendedor.id
        assert presupuesto.resp_vendedor is None

        if request.method == "POST":
            form = ResponderPresupuestoForm(data=request.POST, instance=presupuesto)
            if form.is_valid():
                presupuesto_2 = form.save(commit=False)
                presupuesto_2.resp_vendedor = True
                presupuesto_2.save()
                return redirect("/perfil/"+str(p_vendedor.id))
            else:
                return render(request, "responderPresupuesto.html", {
                    "form": form,
                    "pk": pk
                })
        else:
            form = ResponderPresupuestoForm(instance=presupuesto)
            return render(request, "responderPresupuesto.html", {
                    "form": form,
                    "pk": pk
            })
    except:
        return redirect('error_url')

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
            return redirect("/login")

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

    #try:
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
    #except:
     #   return redirect('error_url')

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

@login_required(login_url="/login/")
def subir_imagenes_prueba_compra(request, pk):

    try:
        user = User.objects.get(pk=request.user.id)
        perfil = Perfil.objects.get(usuario=user)
        compra = Compra.objects.get(pk=pk)
        assert perfil == compra.vendedor
        assert len(list(ImgPrueba.objects.filter(compra=compra))) == 0

        if request.method == "POST":
            form = ImagenesPruebaForm(request.POST, request.FILES)
            files = request.FILES.getlist('imagen')
            if form.is_valid():
                for i in files:
                    img_prueba = ImgPrueba(imagen=i, compra=compra)
                    img_prueba.save()
                return redirect('/impresion/listarVentas')
        else:
            form = ImagenesPruebaForm()
            return render(request, 'subirImagenesPrueba.html', {'form': form})
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
                if not categorias:
                   categorias =Categoria.objects.filter(pk=13)
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
            else:
                return render(request, 'impresiones/editarImpresion.html', {
                'formulario1': form_impresion,
                'imagenes': imagenes_impresion,
                'pk': pk
            })
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

        query = Perfil.objects.all().exclude(impresion__isnull=True)

        if request.method == "POST":
            form = BuscarUsuariosForm(request.POST)
            if form.is_valid():
                nombre = form.cleaned_data.get("nombre")
                query = query.filter(nombre__icontains=nombre)
                query = query.order_by('-es_afiliado')
                return render(request, "registration/listarUsuarios.html", {"form": form, "query": query})
        else:
            form = BuscarUsuariosForm()
            query = query.order_by('-es_afiliado')
            return render(request, "registration/listarUsuarios.html", {"form": form, "query": query})

def detalles_compra(request, pk):

    try:
        impresion = Impresion.objects.get(pk=pk)
        comprador = usuario_logueado(request)
        assert comprador != impresion.vendedor

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
                        'impresion':impresion,'direccion':direccion, 'vistaPaypal': vistaPaypal, 'precio':precio})
        else:
            precio = impresion.precio + 1
            form = DireccionForm()
            form.fields['direccion'].queryset = DirecPerfil.objects.filter(perfil=comprador)
            
        vistaPaypal = False

        return render(request, "impresiones/facturarCompra.html", {"form": form, "perfil": comprador, 'impresion':impresion, 'vistaPaypal': vistaPaypal,'precio':precio})

    except:
       return redirect('error_url')
   
@csrf_exempt
def mostrar_perfil(request, pk):
    try:
        perfil = Perfil.objects.get(pk=pk)
        direcciones = DirecPerfil.objects.all().filter(perfil=perfil)
        impresiones = Impresion.objects.all().filter(vendedor=perfil)
        return render(request, 'perfil.html', {'perfil':perfil, 'direcciones':direcciones,
         'impresiones':impresiones})

    except:
        return redirect('error_url')


def listar_presupuestos_enviados(request):
    try:
        perfil = usuario_logueado(request)

        presupuestos_enviados = Presupuesto.objects.all().filter(interesado=perfil)

        return render(request, 'presupuestos/enviados.html', {'presupuestos':presupuestos_enviados})

    except:
        return redirect('error_url')

def listar_presupuestos_recibidos(request):
    try:
        perfil = usuario_logueado(request)

        presupuestos_recibidos = Presupuesto.objects.all().filter(vendedor=perfil)

        return render(request, 'presupuestos/recibidos.html', {'presupuestos':presupuestos_recibidos})
    
    except:
        return redirect('error_url')
        
def rechazar_presupuesto_interesado(request, pk):
    try:
        perfil = usuario_logueado(request)
        presupuesto = Presupuesto.objects.get(pk=pk)

        assert presupuesto.resp_vendedor == True
        assert presupuesto.resp_interesado == None
        assert perfil == presupuesto.interesado

        presupuesto.resp_interesado = False
        presupuesto.save()

        presupuestos = Presupuesto.objects.all().filter(interesado=perfil)

        return render(request, 'presupuestos/enviados.html', {'presupuestos':presupuestos})
    
    except:
        return redirect('error_url')

def rechazar_presupuesto_vendedor(request, pk):
    try:
        perfil = usuario_logueado(request)
        presupuesto = Presupuesto.objects.get(pk=pk)

        assert not presupuesto.resp_vendedor == True
        assert not presupuesto.resp_vendedor == False
        assert perfil == presupuesto.vendedor

        presupuesto.resp_vendedor = False
        presupuesto.save()

        presupuestos = Presupuesto.objects.all().filter(vendedor=perfil)

        return render(request, 'presupuestos/recibidos.html', {'presupuestos':presupuestos})

    except:
        return redirect('error_url')

def aceptar_presupuesto_interesado(request, pk):

    try:
        usuario= usuario_logueado(request)
        presupuesto= Presupuesto.objects.get(id=pk)
        assert presupuesto.interesado == usuario
        assert presupuesto.resp_vendedor == True
        assert presupuesto.resp_interesado == None
        return detalles_presupuesto(request, presupuesto.id)
    except:
        return redirect('error_url')

def detalles_presupuesto(request, pk):

    try:
        presupuesto = Presupuesto.objects.get(pk=pk)
        comprador = usuario_logueado(request)
        assert comprador == presupuesto.interesado

        if request.method == "POST":
            form = DireccionForm(request.POST)
            if form.is_valid():
                direccionSeleccionada = form.cleaned_data.get("direccion")
                direccion = DirecPerfil.objects.get(direccion=direccionSeleccionada)

                precio = presupuesto.precio + 1
                idPresupuesto = str(pk)

                paypal_dict = {
                    "business": "treeD@business.example.com",
                    "amount": str(precio),
                    "item_name": presupuesto.peticion,
                    "currency_code": "EUR",
                    "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                    "return": request.build_absolute_uri(reverse('comprarPresupuesto_url' , args=[idPresupuesto, direccion.id])),
                    "cancel_return": request.build_absolute_uri(reverse('mostrarPresupuesto_url', args=[idPresupuesto])),
                }

                if settings.DEBUG == False:
                    formPago = PayPalEncryptedPaymentsForm(initial=paypal_dict)
                else:
                    formPago = PayPalPaymentsForm(initial=paypal_dict)

                vistaPaypal = True

                return render(request, "presupuestos/facturarCompra.html", {"formPago": formPago, "perfil": comprador, 
                        'presupuesto':presupuesto, 'direccion':direccion, 'vistaPaypal': vistaPaypal, 'precio':precio})
        else:
            precio = presupuesto.precio + 1
            form = DireccionForm()
            form.fields['direccion'].queryset = DirecPerfil.objects.filter(perfil=comprador)
            
        vistaPaypal = False

        return render(request, "presupuestos/facturarCompra.html", {"form": form, "perfil": comprador, 'presupuesto':presupuesto, 'vistaPaypal': vistaPaypal, 'precio':precio})

    except:
       return redirect('error_url')

@csrf_exempt
def comprar_presupuesto(request, pk, direccion):

    try:
        presupuesto = Presupuesto.objects.get(pk=pk)
        comprador = usuario_logueado(request)
        direc= DirecPerfil.objects.get(id = direccion)
        
        assert presupuesto.interesado == comprador
        compras = list(Compra.objects.filter(comprador=comprador))
        fecha_actual = date.today()
        
        compra = Compra(
            comprador=comprador,
            vendedor=presupuesto.vendedor,
            nombre_impresion=presupuesto.peticion,
            desc_impresion=presupuesto.descripcion,
            precio_impresion=presupuesto.precio,
            fecha_compra=fecha_actual,
            direccion = direc
        )
        compra.save()
        img= ImgImpresion.objects.get(pk=56)
        imagen = ImgCompra(imagen=img.imagen, compra=compra)
        imagen.save()
        presupuesto.resp_interesado=True
        presupuesto.save()
        compras.append(compra)

        return render(request, 'impresiones/listarCompras.html', {'compras': compras})
        
    except:
        return redirect('error_url')
def mostrarPresupuesto(request, pk):

    try:
        presupuesto = Presupuesto.objects.get(id=pk)
        usuario = usuario_logueado(request)
        assert presupuesto.interesado == usuario or presupuesto.vendedor == usuario
        respuestaInteresado=''
        respuestaVendedor=''
        if presupuesto.resp_interesado == True:
            respuestaInteresado = 'ACEPTADO'
        elif presupuesto.resp_interesado == False:
            respuestaInteresado = 'RECHAZADO'
        else:
            respuestaInteresado = 'PENDIENTE'

        if presupuesto.resp_vendedor == True:
            respuestaVendedor = 'ACEPTADO'
        elif presupuesto.resp_vendedor == False:
            respuestaVendedor = 'RECHAZADO'
        else:
            respuestaVendedor = 'PENDIENTE'

        return render (request, 'presupuestos/mostrarPresupuesto.html', {'presupuesto':presupuesto, 'respuestaInteresado':respuestaInteresado,
                    'respuestaVendedor':respuestaVendedor})
    except:
        return redirect('error_url')
        
@csrf_exempt
def subscribirse(request):

    try:
        usuario = usuario_logueado(request)
        usuario.es_afiliado = True
        usuario.save()
        direcciones = DirecPerfil.objects.all().filter(perfil=usuario)
        impresiones = Impresion.objects.all().filter(vendedor=usuario)
        return render(request, 'perfil.html', {'perfil':usuario, 'direcciones':direcciones,
         'impresiones':impresiones})
    except:
        return redirect('error_url')

def hazte_afiliado(request):
    try:

        if request.user.is_authenticated:
            perfil = usuario_logueado(request)
            paypal_dict = {
                        "cmd": "_xclick-subscriptions",
                        "business": 'treeD@business.example.com',
                        "a3": "10.00",                      
                        "p3": 1,                           
                        "t3": "M",                         
                        "src": "1",                        
                        "sra": "1",                        
                        "item_name": "Subscripcion en TreeD",
                        'custom': perfil.id,     
                        "currency_code": "EUR",
                        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                        "return": request.build_absolute_uri(reverse('subscripcion_url')),
                        "cancel_return": request.build_absolute_uri(reverse('mostrarPerfil_url' , args=[perfil.id])),
                }
            if settings.DEBUG == False:
                formPago = PayPalEncryptedPaymentsForm(initial=paypal_dict)
            else:
                formPago = PayPalPaymentsForm(initial=paypal_dict)
            return render(request, 'hazteAfiliado.html',{"formAfiliado": formPago, 'perfil':perfil})
        else:
            return render(request, 'hazteAfiliado.html')
    except:
        return redirect('error_url')


def ver_respuesta_presupuesto(request, pk):
    try:
        presupuesto = Presupuesto.objects.get(id=pk)
        usuario = usuario_logueado(request)
        assert presupuesto.interesado == usuario or presupuesto.vendedor == usuario
        return render (request, 'presupuestos/mostrarRespuesta.html', {'presupuesto':presupuesto})
    except:
        return redirect('error_url')
