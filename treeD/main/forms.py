""" Aqui se encuentran los formularios usados por los templates y por views.py.
"""

from django import forms
from main.models import Perfil, DirecPerfil, Categoria, ImgPrueba, ImgImpresion, ImgCompra, Impresion, Presupuesto, Opinion
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date
import re


class CrearOpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = {
            'nota',
            'opinion',
        }
        widgets = {
            'nota': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'opinion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Opinion'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        nota = cleaned_data.get("nota")

        if nota < 1 or nota > 5:
            msg = "La nota debe estar entre 1 y 5"
            raise ValidationError({'nota': [msg, ]})

class DateInput(forms.DateInput):
    input_type = 'date'

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.jpeg', '.bmp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Los archivos deben ser imagenes .jpg, .png, .jpeg o .bmp')

class PedirPresupuestoForm(forms.ModelForm):

    tamaño = forms.CharField(label="Tamaño", required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Altura x Anchura'}))
    material = forms.CharField(label="Material", required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Material'}))

    class Meta:
        model = Presupuesto
        fields = {
            'peticion',
            'descripcion',
            'tamaño',
            'material'
        }
        widgets = {
            'peticion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Peticion'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        tamaño = cleaned_data.get("tamaño")
        material = self.cleaned_data.get('material')

        if tamaño !=None and tamaño !="":
            if not re.match("^([1-9]+)([0-9]*) x ([1-9]+)([0-9]*)*$", tamaño):
                #msg = "El tamaño debe de tener la forma Altura x Anchura, por ejemplo 30 x 30 (Con los espacios entre los números y la x)"
                msg1 = "El tamaño debe de cumplir las siguientes condiciones. Tener la forma Altura x Anchura "
                msg2 = "(p.e 30 x 30), tener espacios entre la 'x' (p.e 30 x 30, no 30x30)"
                msg3 = " y no empezar por 0 ni llevar decimales (p.e no se permite 0 x 0 o "
                msg4 = "30,1 x 30,1)"
                msg = msg1 + msg2 + msg3 + msg4
                raise ValidationError({'tamaño': [msg, ]})

        if material !=None and material !="":
            if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", material):
                msg = "El material solo debe contener letras"
                raise ValidationError({'tamaño': [msg, ]})


class ResponderPresupuestoForm(forms.ModelForm):

    fecha_envio = forms.DateField(required=False,
        widget=DateInput(attrs={'class': 'form-control',
                                'placeholder': 'Fecha de envio'})
    )

    precio = forms.DecimalField(
        decimal_places=2,
        widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}))

    class Meta:
        model = Presupuesto
        fields = {
            'precio',
            'notas',
            'fecha_envio',
        }
        widgets = {
            'notas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notas'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        precio = cleaned_data.get("precio")
        fecha_envio = cleaned_data.get("fecha_envio")
        today = date.today()

        if not fecha_envio:
            raise ValidationError((""), code='invalid')

        if precio <= 0:
            msg = "El precio debe ser mayor que 0"
            raise ValidationError({'precio': [msg, ]})

        if fecha_envio <= today:
            msg = "La fecha de envio debe ser posterior a la fecha actual"
            raise ValidationError({'fecha_envio': [msg, ]})


class EditarUsernameForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))

    class Meta:
        model = User
        fields = ('username', )

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")

        if len(username) < 6:
            msg = "El nombre de usuario debe tener al menos 6 caracteres"
            raise ValidationError({'username': [msg, ]})

        if not re.match("^[A-Za-z0-9\u00f1\u00d1]*$", username):
            msg = "El nombre de usuario solo puede contener letras y numeros"
            raise ValidationError({'username': [msg, ]})

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            msg = "El nombre de usuario ya esta en uso"
            raise ValidationError({'username': [msg, ]})


class EditarPasswordForm(forms.Form):

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    check_pw = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        check_pw = cleaned_data.get("check_pw")
        if password != check_pw:
            msg = "La contraseña no coincide"
            raise ValidationError({'password': [msg, ]})

        if len(password) < 8:
            msg = "La contraseña debe tener al menos 8 caracteres"
            raise ValidationError({'password': [msg, ]})

        if not re.match("^[A-Za-z0-9\u00f1\u00d1]*$", password):
            msg = "La contraseña solo puede contener letras y numeros"
            raise ValidationError({'password': [msg, ]})

        if not any(x.isupper() for x in password):
            msg = "La contraseña debe contener al menos una mayuscula"
            raise ValidationError({'password': [msg, ]})


class EditarPerfilForm(forms.ModelForm):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras y símbolos"),
        'apellidos_letters': ("Los apellidos solo pueden contener letras y símbolos"),
    }

    nombre = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    apellidos = forms.CharField(label="Apellidos", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Apellidos'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    email_paypal = forms.CharField(label="Email de Paypal", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email de Paypal'}))
    descripcion = forms.CharField(label="Descripción", required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Descripcion', 'rows': 4}))
    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'multiple': False, 'class': 'form-control-file'}),
            validators=[validate_file_extension]
    )

    class Meta:
        model = Perfil
        fields = (
            "nombre",
            "apellidos",
            "descripcion",
            "imagen",
            "email",
            "email_paypal",
        )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", nombre):
            raise forms.ValidationError(
                self.error_messages['nombre_letters'],
                code='nombre_letters',
            )
        return nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", apellidos):
            raise forms.ValidationError(
                self.error_messages['apellidos_letters'],
                code='apellidos_letters',
            )
        return apellidos

    def __init__(self, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].required = False
        self.fields['imagen'].required = False


class AñadirDirecPerfilForm(forms.Form):
    error_messages = {
        'codigo_postal_error': ("El codigo postal debe tener 5 números"),
        'ciudad_error': ("La ciudad solamente puede contener letras"),
        'localidad_error': ("La localidad solamente puede contener letras"),
    }
    ciudad = forms.CharField(label="Ciudad", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Sevilla'}))
    localidad = forms.CharField(label="Localidad", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Sevilla'}))
    calle = forms.CharField(label="Calle o avenida", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'C/Carretera Carmona'}))
    numero = forms.CharField(label="Portal y número", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nº27 2ºIzq'}))
    codigo_postal = forms.CharField(label="Código postal", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '41008'}))

    def clean_codigo_postal(self):
        codigo_postal = self.cleaned_data.get('codigo_postal')

        if not re.match("^[0-9]{5}$", codigo_postal):
            raise forms.ValidationError(
                self.error_messages['codigo_postal_error'],
                code='codigo_postal_error',
            )
        return codigo_postal
    
    def clean_ciudad(self):
        ciudad = self.cleaned_data.get('ciudad')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", ciudad):
            raise forms.ValidationError(
                self.error_messages['ciudad_error'],
                code='ciudad_error',
            )
        return ciudad
    
    def clean_localidad(self):
        localidad = self.cleaned_data.get('localidad')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", localidad):
            raise forms.ValidationError(
                self.error_messages['localidad_error'],
                code='localidad_error',
            )
        return localidad

class GDPRForm(forms.Form):
    checkbox = forms.BooleanField(label="", required=True, widget=forms.CheckboxInput())

class BuscadorForm(forms.Form):

    """ Formulario del buscador. Campos.
    - nombre: el buscador busca impresiones que contenga la palabra/s contenidas en 'Nombre'
    - categorias: el buscador busca impresiones que contengan las categorias seleccionadas
    - precio_min: el buscador busca impresiones cuyo precio sea mayor que precio_min
    - precio_max: el buscador busca impresiones cuyo precio sea menor que precio_max
    """

    nombre = forms.CharField(
        label='Nombre de la impresion',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control w-50 mr-2',
                   'placeholder': 'Buscar Impresiones 3D'}
        )
    )
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    precio_min = forms.DecimalField(
        label='Precio Minimo',
        required=False,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control w-100 ',
                   'placeholder': 'Precio Minimo'}
        )
    )
    precio_max = forms.DecimalField(
        label='Precio Maximo',
        required=False,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control w-100 ',
                   'placeholder': 'Precio Maximo'}
        )
    )

    def clean(self):
        """Valida si esta bien el rango de precio.
        """
        cleaned_data = self.cleaned_data
        precio_min = cleaned_data.get("precio_min")
        precio_max = cleaned_data.get("precio_max")
        if precio_min is not None and precio_max is not None:
            if precio_min >= precio_max:
                msg = "El precio minimo no puede ser mayor que el precio maximo"
                raise ValidationError({'precio_min': [msg, ]})


class ImpresionForm(forms.ModelForm):

    precio = forms.DecimalField(
        decimal_places=2,
        widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}))

    class Meta:
        model = Impresion
        fields = {
            'nombre',
            'descripcion',
            'precio',
            'categorias',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo'}),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Descripcion', 'rows': 4}),
            'categorias': forms.CheckboxSelectMultiple(),

        }

    def clean(self):
        """Valida si el precio es positivo.
        """
        cleaned_data = self.cleaned_data
        precio = cleaned_data.get("precio")

        if precio <= 0:
            msg = "El precio debe ser mayor que 0"
            raise ValidationError({'precio': [msg, ]})


    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['categorias'].required = False


class CargarImagenForm(forms.ModelForm):
    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'multiple': True, 'class': 'form-control-file'}),
            validators=[validate_file_extension]
    )

    class Meta:
        model = ImgImpresion
        fields = ('imagen',)


class ImagenesPruebaForm(forms.Form):
    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'multiple': False, 'class': 'form-control-file'}),
            validators=[validate_file_extension]
    )

class CodigoForm(forms.Form):
    error_messages = {
        'empresa_envio_error': ("La empresa solo puede contener letras"),
    }
    codigo_envio = forms.CharField(label='Código de envío', required=False,
    widget=forms.TextInput(attrs={'class': 'form-control w-100 mr-2', 'placeholder': 'Código de envío'}))

    empresa_envio = forms.CharField(label='Empresa encargada del envío', required=True,
    widget=forms.TextInput(attrs={'class': 'form-control w-100 mr-2', 
    'placeholder': 'Correos, AliExpress'})
    )

    def clean_empresa_envio(self):
        empresa_envio = self.cleaned_data.get('empresa_envio')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", empresa_envio):
            raise forms.ValidationError(
                self.error_messages['empresa_envio_error'],
                code='empresa_envio_error',
            )
        return empresa_envio


class BuscarUsuariosForm(forms.Form):

    nombre = forms.CharField(
        label='Nombre del usuario',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control w-50 mr-2',
                   'placeholder': 'Buscar usuarios'}
        )
    )


class DireccionForm(forms.Form):

    direccion = forms.ModelChoiceField(
        label='', queryset=DirecPerfil.objects.all())


class ImagenForm(forms.Form):
    imagen = forms.ImageField(required=False,
                              widget=forms.ClearableFileInput(
                                  attrs={'class': 'form-control-file'}),
                                  validators=[validate_file_extension])


class PerfilForm(forms.ModelForm):
    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras y símbolos"),
        'apellidos_letters': ("Los apellidos solo pueden contener letras y símbolos"),
    }

    class Meta:
        model = Perfil
        fields = {
            'nombre',
            'apellidos',
            'email',
            'descripcion',
            'email_paypal',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'email_paypal': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email de Paypal'}),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 4}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", nombre):
            raise forms.ValidationError(
                self.error_messages['nombre_letters'],
                code='nombre_letters',
            )
        return nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", apellidos):
            raise forms.ValidationError(
                self.error_messages['apellidos_letters'],
                code='apellidos_letters',
            )
        return apellidos
    
    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        self.fields['email_paypal'].required = False


class DirecPerfilForm(forms.ModelForm):
    error_messages = {
        'codigo_postal_error': ("El código postal debe tener 5 números"),
        'ciudad_error': ("La ciudad solamente puede contener letras"),
        'localidad_error': ("La localidad solamente puede contener letras"),
    }
    
    class Meta:
        model = DirecPerfil
        fields = {
            'ciudad',
            'localidad',
            'calle',
            'numero',
            'codigo_postal',
        }
        widgets = {
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sevilla'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sevilla'}),
            'calle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'C/Carretera Carmona'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nº27 2ºIzq'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '41008'}),

        }
    
    def clean_codigo_postal(self):
        codigo_postal = self.cleaned_data.get('codigo_postal')

        if not re.match("^[0-9]{5}$", codigo_postal):
            raise forms.ValidationError(
                self.error_messages['codigo_postal_error'],
                code='codigo_postal_error',
            )
        return codigo_postal

    def clean_ciudad(self):
        ciudad = self.cleaned_data.get('ciudad')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", ciudad):
            raise forms.ValidationError(
                self.error_messages['ciudad_error'],
                code='ciudad_error',
            )
        return ciudad
    
    def clean_localidad(self):
        localidad = self.cleaned_data.get('localidad')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", localidad):
            raise forms.ValidationError(
                self.error_messages['localidad_error'],
                code='localidad_error',
            )
        return localidad


class UserForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': ("Las contraseñas no coinciden"),
        'username_exists': ("Ya existe ese nombre de usuario"),
        'password_short': ("La contraseña debe tener al menos 8 caracteres"),
        'password_letters': ("La contraseña solo puede contener letras y números"),
        'password_capital': ("La contraseña debe tener al menos una mayúscula"),
        'username_short': ("El nombre de usuario debe tener al menos 6 caracteres"),
        'username_letters': ("El nombre de usuario solo puede contener letras y numeros"),
    }

    password1 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label=("Password confirmation"),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'}),
                                help_text=("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'})
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        if len(password1) < 8:
            raise forms.ValidationError(
                self.error_messages['password_short'],
                code='password_short',
            )

        if not re.match("^[A-Za-z0-9\u00f1\u00d1]*$", password1):
            raise forms.ValidationError(
                self.error_messages['password_letters'],
                code='password_letters',
            )

        if not any(x.isupper() for x in password1):
            raise forms.ValidationError(
                self.error_messages['password_capital'],
                code='password_capital',
            )
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 6:
            raise forms.ValidationError(
                self.error_messages['username_short'],
                code='username_short',
            )

        if not re.match("^[A-Za-z0-9\u00f1\u00d1]*$", username):
            raise forms.ValidationError(
                self.error_messages['username_letters'],
                code='username_letters',
            )

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['username_exists'],
                code='username_exists',
            )
        return username

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
