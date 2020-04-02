from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from usuarios.forms import AñadirDirecPerfilForm, EditarUsernameForm, EditarPasswordForm, EditarPerfilForm, DireccionForm, PerfilForm, DirecPerfilForm, UserForm,ImagenForm
from main.models import Impresion
from usuarios.models import Perfil, DirecPerfil
from django.contrib.auth.models import User




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

        return render(request, 'registration/register.html', {
            'form_usuario': form_usuario,
            'form_perfil': form_perfil,
            'form_direccion': form_direccion,
            'form_imagen': form_imagen
        })
    except:
        return redirect('error_url')


@csrf_exempt
def mostrar_perfil(request, pk):
    try:
        perfil = Perfil.objects.get(pk=pk)
        direcciones = DirecPerfil.objects.all().filter(perfil=perfil)
        impresiones = Impresion.objects.all().filter(vendedor=perfil)
        return render(request, 'perfil.html', {'perfil': perfil, 'direcciones': direcciones,
                                               'impresiones': impresiones})

    except:
        return redirect('error_url')