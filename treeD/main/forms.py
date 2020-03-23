""" Aqui se encuentran los formularios usados por los templates y por views.py.
"""

from django import forms
from main.models import Categoria
from main.models import Impresion, ImgImpresion, ImgPrueba
from django.core.exceptions import ValidationError

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
