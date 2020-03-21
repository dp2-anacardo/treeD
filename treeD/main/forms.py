""" Aqui se encuentran los formularios usados por los templates y por views.py.
"""

from django import forms
from main.models import Categoria
from main.models import Impresion, ImgImpresion, Perfil, DirecPerfil
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class EditarUsernameForm(forms.ModelForm):
    username = forms.CharField(label="Username")

    class Meta:
        model = User
        fields = ('username', )

class EditarPasswordForm(forms.Form):
    
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput()
    )
    check_pw = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        check_pw = cleaned_data.get("check_pw")
        if password != check_pw:
            msg = "La contraseña no coincide"
            raise ValidationError({'password': [msg,]})

class EditarPerfilForm(forms.ModelForm):
    nombre = forms.CharField(label="Nombre")
    apellidos = forms.CharField(label="Apellidos")
    descripcion = forms.CharField(label="Descripción", required=False)
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
        )

    def __init__(self, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)        
        self.fields['descripcion'].required = False
        self.fields['imagen'].required = False

class AñadirDirecPerfilForm(forms.Form):
    direccion = forms.CharField(label="Direccion principal")


"""
class EditarUsuarioForm(forms.Form):
    nickname = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput()
    )
    check_pw = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput()
    )
    nombre = forms.CharField(label="Nombre")
    apellidos = forms.CharField(label="Apellidos")
    descripcion = forms.CharField(label="Descripción", required=False)
    direccion1 = forms.CharField(label="Direccion principal")
    direccion2 = forms.CharField(label="Direccion opcional", required=False)
    direccion3 = forms.CharField(label="Direccion opcional", required=False)
    direccion4 = forms.CharField(label="Direccion opcional", required=False)
    direccion5 = forms.CharField(label="Direccion opcional", required=False)
    imagen = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': False, 'class': 'form-control-file'})
    )

    4
"""

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
