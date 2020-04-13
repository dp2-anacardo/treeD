from django.contrib.auth import login, authenticate
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalEncryptedPaymentsForm, PayPalPaymentsForm
from django.urls import reverse
from datetime import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import Perfil, DirecPerfil, Compra, Categoria, ImgPrueba, ImgImpresion, ImgCompra, Impresion, Presupuesto
from main.forms import AñadirDirecPerfilForm, PedirPresupuestoForm, ResponderPresupuestoForm, EditarUsernameForm, EditarPasswordForm, EditarPerfilForm, BuscadorForm, ImpresionForm, CargarImagenForm, ImagenesPruebaForm, BuscarUsuariosForm, DireccionForm, ImagenForm, PerfilForm, DirecPerfilForm, UserForm, GDPRForm
from django.core.paginator import Paginator
import operator




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
            form = ResponderPresupuestoForm(
                data=request.POST, instance=presupuesto)
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
        form_2 = EditarPerfilForm(
            data=request.POST, files=request.FILES, instance=perfil)
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


@login_required(login_url="/login/")
def listar_compras_impresiones(request):

    try:
        usuario = usuario_logueado(request)
        compras = Compra.objects.all().filter(comprador=usuario)
        compras = compras.order_by('-fecha_compra')
        paginator = Paginator(compras, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'impresiones/listarCompras.html', {'compras': page_obj})
    except:
       return redirect('error_url')


def listar_impresiones(request):

    try:
        form = BuscadorForm(request.POST)
        impresiones_no_afiliados = list(
            Impresion.objects.all().filter(vendedor__es_afiliado=False))
        impresiones_afiliados = list(
            Impresion.objects.all().filter(vendedor__es_afiliado=True))
        impresiones_afiliados.extend(impresiones_no_afiliados)
        paginator = Paginator(impresiones_afiliados, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        categorias = Categoria.objects.all()
        return render(request, 'impresiones/listarImpresiones.html', {
            'impresiones': page_obj,
            'categorias': categorias,
            'form': form
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
            return render(request, 'subirImagenesPrueba.html', {'form': form})
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
            form_gdpr = GDPRForm(request.POST)
            if form_usuario.is_valid() and form_perfil.is_valid() and form_imagen.is_valid() and form_direccion.is_valid and form_gdpr:

                usuario = form_usuario.save()
                perfil = form_perfil.save(commit=False)
                perfil.usuario = usuario
                if form_imagen.cleaned_data['imagen'] is not None:
                    imagen = request.FILES['imagen']
                    perfil.imagen = imagen
                perfil.es_afiliado = False
                perfil.save()

                direccion = form_direccion.save(commit=False)
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
            form_imagen = ImagenForm()
            form_gdpr = GDPRForm()

        return render(request, 'registration/register.html', {
            'form_usuario': form_usuario,
            'form_perfil': form_perfil,
            'form_direccion': form_direccion,
            'form_imagen': form_imagen,
            'form_gdpr': form_gdpr
        })
    except:
        return redirect('error_url')


@login_required(login_url="/login/")
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
                    categorias = Categoria.objects.filter(pk=13)
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
            form_imagen = CargarImagenForm()
        return render(request, 'impresiones/crearImpresion.html', {
            'formulario1': form_impresion,
            'formulario_imagen': form_imagen
        })
    except:
        return redirect('error_url')


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def listar_impresiones_publicadas(request):
    
    if request.user.is_authenticated:
        perfil_user = Perfil.objects.get(usuario=request.user)
        query = Impresion.objects.filter(vendedor=perfil_user)
        paginator=Paginator(query, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "misPublicaciones.html", {"query": page_obj})

    return render(request, 'index.html')


@csrf_exempt
def comprar_impresion_3d(request, pk, direccion):

    try:
        impresion = Impresion.objects.get(pk=pk)
        comprador = usuario_logueado(request)
        direc = DirecPerfil.objects.get(id=direccion)

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
            direccion=direc,
            pagado=False
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
            paginator = Paginator(query, 6)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

    else:
        paginator = Paginator(query, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = BuscadorForm()

    return render(request, "impresiones/listarImpresiones.html", {"form": form, "impresiones": page_obj})


@login_required(login_url="/login/")
def listar_ventas_realizadas(request):

    if request.user.is_authenticated:
        perfil_user = Perfil.objects.get(usuario=request.user)
        query = Compra.objects.filter(vendedor=perfil_user)
        query = query.order_by('-fecha_compra')
        paginator = Paginator(query, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "impresiones/listarVentas.html", {"query": page_obj})
    return render(request, 'index.html')


def buscar_usuarios(request):

    query = Perfil.objects.all().exclude(impresion__isnull=True)

    if request.method == "POST":
        form = BuscarUsuariosForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get("nombre")
            query = query.filter(usuario__username__icontains=nombre)
            query = query.order_by('-es_afiliado')
            paginator = Paginator(query, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "registration/listarUsuarios.html", {"form": form, "query": page_obj})
    else:
        form = BuscarUsuariosForm()
        query = query.order_by('-es_afiliado')
        paginator = Paginator(query, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "registration/listarUsuarios.html", {"form": form, "query": page_obj})


def detalles_compra(request, pk):

    try:
        impresion = Impresion.objects.get(pk=pk)
        comprador = usuario_logueado(request)
        assert comprador != impresion.vendedor

        if request.method == "POST":
            form = DireccionForm(request.POST)
            if form.is_valid():
                direccionSeleccionada = form.cleaned_data.get("direccion")
                direccion = DirecPerfil.objects.get(
                    id=direccionSeleccionada.id)

                precio = impresion.precio + 1
                idImpresion = str(pk)

                paypal_dict = {
                    "business": "treeD@business.example.com",
                    "amount": str(precio),
                    "item_name": impresion.nombre,
                    "currency_code": "EUR",
                    "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                    "return": request.build_absolute_uri(reverse('comprarImpresion_url', args=[idImpresion, direccion.id])),
                    "cancel_return": request.build_absolute_uri(reverse('mostrarImpresion_url', args=[idImpresion])),
                }

                if settings.DEBUG == False:
                    formPago = PayPalEncryptedPaymentsForm(initial=paypal_dict)
                else:
                    formPago = PayPalPaymentsForm(initial=paypal_dict)

                vistaPaypal = True

                return render(request, "impresiones/facturarCompra.html", {"formPago": formPago, "perfil": comprador,
                                                                           'impresion': impresion, 'direccion': direccion, 'vistaPaypal': vistaPaypal, 'precio': precio})
        else:
            precio = impresion.precio + 1
            form = DireccionForm()
            form.fields['direccion'].queryset = DirecPerfil.objects.filter(
                perfil=comprador)

        vistaPaypal = False

        return render(request, "impresiones/facturarCompra.html", {"form": form, "perfil": comprador, 'impresion': impresion, 'vistaPaypal': vistaPaypal, 'precio': precio})

    except:
        return redirect('error_url')


@csrf_exempt
def mostrar_perfil(request, pk):
    try:
        perfil = Perfil.objects.get(pk=pk)
        direcciones = DirecPerfil.objects.all().filter(perfil=perfil)
        impresiones = Impresion.objects.all().filter(vendedor=perfil)
        paginator = Paginator(impresiones, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'perfil.html', {'perfil': perfil, 'direcciones': direcciones,
                                               'impresiones': page_obj})
    except:
        return redirect('error_url')


@login_required(login_url="/login/")
def listar_presupuestos_enviados(request):
    try:
        perfil = usuario_logueado(request)
        presupuestos_enviados = Presupuesto.objects.all().filter(interesado=perfil)
        paginator = Paginator(presupuestos_enviados, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'presupuestos/enviados.html', {'presupuestos': page_obj})

    except:
        return redirect('error_url')


@login_required(login_url="/login/")
def listar_presupuestos_recibidos(request):
    try:
        perfil = usuario_logueado(request)
        presupuestos_recibidos = Presupuesto.objects.all().filter(vendedor=perfil)
        paginator = Paginator(presupuestos_recibidos, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'presupuestos/recibidos.html', {'presupuestos': page_obj})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
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

        return render(request, 'presupuestos/enviados.html', {'presupuestos': presupuestos})

    except:
        return redirect('error_url')


@login_required(login_url="/login/")
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

        return render(request, 'presupuestos/recibidos.html', {'presupuestos': presupuestos})

    except:
        return redirect('error_url')


@login_required(login_url="/login/")
def aceptar_presupuesto_interesado(request, pk):

    try:
        usuario = usuario_logueado(request)
        presupuesto = Presupuesto.objects.get(id=pk)
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
                direccion = DirecPerfil.objects.get(
                    id=direccionSeleccionada.id)

                precio = presupuesto.precio + 1
                idPresupuesto = str(pk)

                paypal_dict = {
                    "business": "treeD@business.example.com",
                    "amount": str(precio),
                    "item_name": presupuesto.peticion,
                    "currency_code": "EUR",
                    "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                    "return": request.build_absolute_uri(reverse('comprarPresupuesto_url', args=[idPresupuesto, direccion.id])),
                    "cancel_return": request.build_absolute_uri(reverse('mostrarRespuesta_url', args=[idPresupuesto])),
                }

                if settings.DEBUG == False:
                    formPago = PayPalEncryptedPaymentsForm(initial=paypal_dict)
                else:
                    formPago = PayPalPaymentsForm(initial=paypal_dict)

                vistaPaypal = True

                return render(request, "presupuestos/facturarCompra.html", {"formPago": formPago, "perfil": comprador,
                                                                            'presupuesto': presupuesto, 'direccion': direccion, 'vistaPaypal': vistaPaypal, 'precio': precio})
        else:
            precio = presupuesto.precio + 1
            form = DireccionForm()
            form.fields['direccion'].queryset = DirecPerfil.objects.filter(
                perfil=comprador)

        vistaPaypal = False

        return render(request, "presupuestos/facturarCompra.html", {"form": form, "perfil": comprador, 'presupuesto': presupuesto, 'vistaPaypal': vistaPaypal, 'precio': precio})

    except:
        return redirect('error_url')


@csrf_exempt
def comprar_presupuesto(request, pk, direccion):

    try:
        presupuesto = Presupuesto.objects.get(pk=pk)
        comprador = usuario_logueado(request)
        direc = DirecPerfil.objects.get(id=direccion)

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
            direccion=direc,
            pagado=False
        )
        compra.save()
        img = ImgImpresion.objects.get(pk=56)
        imagen = ImgCompra(imagen=img.imagen, compra=compra)
        imagen.save()
        presupuesto.resp_interesado = True
        presupuesto.save()
        compras.append(compra)

        return render(request, 'impresiones/listarCompras.html', {'compras': compras})

    except:
        return redirect('error_url')


@login_required(login_url="/login/")
def mostrarPresupuesto(request, pk):

    try:
        presupuesto = Presupuesto.objects.get(id=pk)
        usuario = usuario_logueado(request)
        assert presupuesto.interesado == usuario or presupuesto.vendedor == usuario
        respuestaInteresado = ''
        respuestaVendedor = ''
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

        return render(request, 'presupuestos/mostrarPresupuesto.html', {'presupuesto': presupuesto, 'respuestaInteresado': respuestaInteresado,
                                                                        'respuestaVendedor': respuestaVendedor})
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
        return render(request, 'perfil.html', {'perfil': usuario, 'direcciones': direcciones,
                                               'impresiones': impresiones})
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
                "cancel_return": request.build_absolute_uri(reverse('mostrarPerfil_url', args=[perfil.id])),
            }
            if settings.DEBUG == False:
                formPago = PayPalEncryptedPaymentsForm(initial=paypal_dict)
            else:
                formPago = PayPalPaymentsForm(initial=paypal_dict)
            return render(request, 'hazteAfiliado.html', {"formAfiliado": formPago, 'perfil': perfil})
        else:
            return render(request, 'hazteAfiliado.html')
    except:
        return redirect('error_url')


@login_required(login_url="/login/")
def ver_respuesta_presupuesto(request, pk):
    try:
        presupuesto = Presupuesto.objects.get(id=pk)
        usuario = usuario_logueado(request)
        assert presupuesto.interesado == usuario or presupuesto.vendedor == usuario
        return render(request, 'presupuestos/mostrarRespuesta.html', {'presupuesto': presupuesto})
    except:
        return redirect('error_url')

def estadisticas_venta(request):

    try:
        usuario = usuario_logueado(request)
        assert usuario.es_afiliado == True

        num_ventas_totales=Compra.objects.filter(vendedor=usuario).count()
        mes = datetime.now().month
        num_ventas_mensuales=Compra.objects.filter(vendedor=usuario).filter(fecha_compra__month = mes).count()
        productos= Compra.objects.filter(vendedor=usuario).filter(pagado=True)
        num_ganancias_totales=0
        for c in productos:
            num_ganancias_totales = num_ganancias_totales + (c.precio_impresion - (0.1*c.precio_impresion))
        productosMensuales= Compra.objects.filter(vendedor=usuario).filter(pagado=True).filter(fecha_compra__month = mes)
        num_ganancias_mensuales=0
        for c in productosMensuales:
            num_ganancias_mensuales = num_ganancias_mensuales + (c.precio_impresion - (0.1*c.precio_impresion))
        productosPendientesPago=Compra.objects.filter(vendedor=usuario).filter(pagado=False)
        num_ganancias_pendientes=0
        for c in productosPendientesPago:
            num_ganancias_pendientes=num_ganancias_pendientes + (c.precio_impresion - (0.1*c.precio_impresion))
        misImpresiones= Impresion.objects.filter(vendedor=usuario)
        compras=[]
        nombres = []
        
        for i in misImpresiones:
            numeroCompras= Compra.objects.filter(vendedor=usuario).filter(nombre_impresion=i.nombre).count()
            compras.append(numeroCompras)
        
        diccionario = dict(zip(misImpresiones,compras))
        top = sorted(diccionario.items(), key=operator.itemgetter(1), reverse=True)
        
        compras2=[]
        for par in top:
            if len(nombres) == 5:
                break
            nombres.append(par[0].nombre)
            compras2.append(par[1])
    
        return render(request, 'registration/estadisticasVenta.html',{'VentasTotales':num_ventas_totales,
                    'VentasMensuales':num_ventas_mensuales, 'GananciasTotales':num_ganancias_totales,
                    'GananciasMensuales':num_ganancias_mensuales,'ProductosPendientesPago':productosPendientesPago,
                    'GananciasPendientes':num_ganancias_pendientes, 'misImpresiones':nombres,'numeroCompras':compras2})
    except:
        return redirect('error_url')

def gdpr(request):
    return render(request, 'terminosYCondiciones.html')
