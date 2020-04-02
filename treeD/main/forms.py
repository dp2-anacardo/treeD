""" Aqui se encuentran los formularios usados por los templates y por views.py.
"""

from django import forms
from main.models import Perfil, DirecPerfil, Categoria, ImgPrueba, ImgImpresion, ImgCompra, Impresion, Presupuesto
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date
import re


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
    class Meta:
        model = Presupuesto
        fields = {
            'peticion',
            'descripcion',
        }
        widgets = {
            'peticion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Peticion'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
        }


class ResponderPresupuestoForm(forms.ModelForm):
    fecha_envio = forms.DateField(
        widget=DateInput(attrs={'class': 'form-control',
                                'placeholder': 'Fecha de envio'})
    )

    class Meta:
        model = Presupuesto
        fields = {
            'precio',
            'notas',
            'fecha_envio',
        }
        widgets = {
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notas'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        precio = cleaned_data.get("precio")
        fecha_envio = cleaned_data.get("fecha_envio")
        today = date.today()

        if precio <= 0:
            msg = "El precio debe ser mayor que 0"
            raise ValidationError({'precio': [msg, ]})

        if fecha_envio <= today:
            msg = "La fecha de envio debe ser posterior a la fecha actual"
            raise ValidationError({'fecha_envio': [msg, ]})



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
                   'placeholder': 'Buscar Piezas 3D'}
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
            attrs={'class': 'form-control w-100 ',
                   'placeholder': 'Precio Minimo'}
        )
    )
    precio_max = forms.FloatField(
        label='Precio Maximo',
        required=False,
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
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
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


class BuscarUsuariosForm(forms.Form):

    nombre = forms.CharField(
        label='Nombre del usuario',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control w-50 mr-2',
                   'placeholder': 'Buscar usuarios'}
        )
    )


