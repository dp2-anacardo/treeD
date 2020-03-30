""" Aqui se encuentran los formularios usados por los templates y por views.py.
"""

from django import forms
from main.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date
import re

class DateInput(forms.DateInput):
    input_type = 'date'

class PedirPresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = {
            'peticion',
            'descripcion',
        }
        widgets = {
            'peticion':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Peticion'}),
            'descripcion':forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Descripcion'}),
        }

class ResponderPresupuestoForm(forms.ModelForm):
    fecha_envio = forms.DateField(
        widget=DateInput(attrs={'class': 'form-control', 'placeholder':'Fecha de envio'})
    )

    class Meta:
        model = Presupuesto
        fields = {
            'precio',
            'notas',
            'fecha_envio',
        }
        widgets = {
            'precio':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Precio'}),
            'notas':forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Notas'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        precio = cleaned_data.get("precio")
        fecha_envio = cleaned_data.get("fecha_envio")
        today = date.today()

        if precio <= 0:
            msg = "El precio debe ser mayor que 0"
            raise ValidationError({'precio': [msg,]})

        if fecha_envio <= today:
            msg = "La fecha de envio debe ser posterior a la fecha actual"
            raise ValidationError({'fecha_envio': [msg,]})

class EditarUsernameForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'}))

    class Meta:
        model = User
        fields = ('username', )

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")

        if len(username) < 6:
            msg = "El nombre de usuario debe tener al menos 6 caracteres"
            raise ValidationError({'username': [msg,]})

        if not re.match("^[A-Za-z0-9]*$", username):
            msg = "El nombre de usuario solo puede contener letras y numeros"
            raise ValidationError({'username': [msg,]})

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            msg = "El nombre de usuario ya esta en uso"
            raise ValidationError({'username': [msg,]})


class EditarPasswordForm(forms.Form):
    
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'})
    )
    check_pw = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'})
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        check_pw = cleaned_data.get("check_pw")
        if password != check_pw:
            msg = "La contraseña no coincide"
            raise ValidationError({'password': [msg,]})

        if len(password) < 8:
            msg = "La contraseña debe tener al menos 8 caracteres"
            raise ValidationError({'password': [msg,]})

        if not re.match("^[A-Za-z0-9]*$", password):
            msg = "La contraseña solo puede contener letras y numeros"
            raise ValidationError({'password': [msg,]})

        if not any(x.isupper() for x in password):
            msg = "La contraseña debe contener al menos una mayuscula"
            raise ValidationError({'password': [msg,]})

class EditarPerfilForm(forms.ModelForm):
    nombre = forms.CharField(label="Nombre",widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Nombre'}))
    apellidos = forms.CharField(label="Apellidos",widget = forms.TextInput(attrs={'class': 'form-control','placeholder':'Apellidos'}))
    email = forms.CharField(label="Email",widget = forms.TextInput(attrs={'class': 'form-control','placeholder':'email'}))
    descripcion = forms.CharField(label="Descripción", required=False,widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Descripcion','rows':4}))
    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': False, 'class': 'form-control-file'})
    )

    class Meta:
        model = Perfil
        fields = (
            "nombre",
            "apellidos",
            "descripcion",
            "imagen",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)        
        self.fields['descripcion'].required = False
        self.fields['imagen'].required = False

class AñadirDirecPerfilForm(forms.Form):
    direccion = forms.CharField(label="Direccion principal",widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ciudad, Calle Nº, CP'}))
import re

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
            attrs={'class': 'form-control w-50 mr-2', 'placeholder': 'Buscar Piezas 3D'}
        )
    )
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    precio_min = forms.FloatField(
        label='Precio Minimo',
        required=False,
        widget=forms.NumberInput(
            attrs={'class': 'form-control w-100 ', 'placeholder': 'Precio Minimo'}
        )
    )
    precio_max = forms.FloatField(
        label='Precio Maximo',
        required=False,
        widget=forms.NumberInput(
            attrs={'class': 'form-control w-100 ', 'placeholder': 'Precio Maximo'}
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
                raise ValidationError({'precio_min': [msg,]})

class ImpresionForm(forms.ModelForm):
    class Meta:
        model = Impresion
        fields = {
            'nombre',
            'descripcion',
            'precio',
            'categorias',
        }
        widgets = {
            'nombre':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Titulo'}),
            'descripcion':forms.Textarea(
                attrs={'class':'form-control', 'placeholder':'Descripcion', 'rows':4}),
            'precio':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Precio'}),
            'categorias':forms.CheckboxSelectMultiple(),

        }
    def clean(self):
        """Valida si el precio es positivo.
        """
        cleaned_data = self.cleaned_data
        precio = cleaned_data.get("precio")

        if precio <= 0:
            msg = "Precio no valido"
            raise ValidationError({'precio': [msg,]})

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['categorias'].required = False

class CargarImagenForm(forms.ModelForm):
    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control-file'})
    )
    class Meta:
        model = ImgImpresion
        fields = ('imagen',)

class ImagenesPruebaForm(forms.Form):
    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': False, 'class': 'form-control-file'})
    )

class BuscarUsuariosForm(forms.Form):
    
    nombre = forms.CharField(
        label='Nombre del usuario',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control w-50 mr-2', 'placeholder': 'Buscar usuarios'}
        )
    )
class DireccionForm(forms.Form):
    
    direccion = forms.ModelChoiceField(label='',queryset=DirecPerfil.objects.all())
class ImagenForm(forms.Form):
    imagen = forms.ImageField(required=False,
        widget=forms.ClearableFileInput(attrs={ 'class': 'form-control-file'})
    )

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = {
            'nombre',
            'apellidos',
            'email',
            'descripcion',
        }
        widgets = {
            'nombre':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre'}),
            'apellidos':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Apellidos'}),
            'email':forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email'}),
            'descripcion':forms.Textarea(
                attrs={'class':'form-control', 'placeholder':'Descripción', 'rows':4}),
        }

class DirecPerfilForm(forms.ModelForm):
    class Meta:
        model = DirecPerfil
        fields = {
            'direccion',
        }
        widgets = {
            'direccion':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Ciudad, Calle Nº, CP'}),
        }

class UserForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': ("Las contraseñas no coinciden"),
        "username_exists": ("Ya existe ese nombre de usuario"),
        'password_short': ("La contraseña debe tener al menos 8 caracteres"),
        'password_letters': ("La contraseña solo puede contener letras y números"),
        'password_capital': ("La contraseña debe tener al menos una mayúscula"),
        'username_short': ("El nombre de usuario debe tener al menos 6 caracteres"),
        'username_letters': ("El nombre de usuario solo puede contener letras y numeros"),
    }

    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}))
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirme su contraseña'}),
        help_text=("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)
        widgets = {
            'username':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre de Usuario'})
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

        if not re.match("^[A-Za-z0-9]*$", password1):
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

        if not re.match("^[A-Za-z0-9]*$", username):
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
