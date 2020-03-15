""" Aqui se encuentran los formularios usados por los templates y por views.py
"""

from django import forms
from django.core.exceptions import ValidationError
from main.models import Categoria
from django import forms
from main.models import Impresion, Imagen
from django.core.exceptions import ValidationError

class BuscadorForm(forms.Form):

    """ Formulario del buscador. Campos:
    - nombre: el buscador busca impresiones que contenga la palabra/s contenidas en 'Nombre'
    - categorias: el buscador busca impresiones que contengan las categorias seleccionadas
    - precio_min: el buscador busca impresiones cuyo precio sea mayor que precio_min
    - precio_max: el buscador busca impresiones cuyo precio sea menor que precio_max
    """

    nombre = forms.CharField(label='Nombre de la impresion', required=False,widget=forms.TextInput(attrs={'class': 'form-control w-50 mr-2','placeholder': 'Buscar Piezas 3D'}))
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects, widget=forms.CheckboxSelectMultiple(), required=False)
    precio_min = forms.FloatField(label='Precio Minimo', required=False,widget=forms.NumberInput(attrs={'class': 'form-control w-100 ','placeholder': 'Precio Minimo'}))
    precio_max = forms.FloatField(label='Precio Maximo', required=False,widget=forms.NumberInput(attrs={'class': 'form-control w-100 ','placeholder': 'Precio Maximo'}))

    def clean(self):
        """Valida si esta bien el rango de precio
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
    def clean(self):
        """Valida si el precio es positivo
        """
        cleaned_data = self.cleaned_data
        precio = cleaned_data.get("precio")

        if precio <= 0:
            msg = "Precio no valido"
            raise ValidationError({'precio': [msg,]})

class CargarImagenForm(forms.ModelForm):
    imagen = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))    
    class Meta:
        model = Imagen
        fields = ('imagen', )
        

