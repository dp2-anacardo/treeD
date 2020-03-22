""" Aqui se encuentran los formularios usados por los templates y por views.py.
"""

from django import forms
from main.models import Categoria
from main.models import Impresion, ImgImpresion, Perfil, DirecPerfil
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

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
            'direccion':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Dirección'}),
        }

class UserForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': ("Las contraseñas no coinciden"),
        "username_exists": ("Ya existe ese nombre de usuario"),
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
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            User._default_manager.get(username=username)
            #if the user exists, then let's raise an error message

            raise forms.ValidationError( 
            self.error_messages['username_exists'],  #my error message
            code='username_exists',   #set the error message key
                )
        except User.DoesNotExist:
            return username # if user does not exist so we can continue the registration process

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user