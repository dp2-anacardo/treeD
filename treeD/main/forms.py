""" Aqui se encuentran los formularios usados por los templates y por views.py
"""

from django import forms
from django.core.exceptions import ValidationError
from main.models import Categoria

class BuscadorForm(forms.Form):

    """ Formulario del buscador. Campos:
    - nombre: el buscador busca impresiones que contenga la palabra/s contenidas en 'Nombre'
    - categorias: el buscador busca impresiones que contengan las categorias seleccionadas
    - precio_min: el buscador busca impresiones cuyo precio sea mayor que precio_min
    - precio_max: el buscador busca impresiones cuyo precio sea menor que precio_max
    """

    CATEGORIAS = [(c.idCategoria, c.categoria) for c in Categoria.objects.all()]

    nombre = forms.CharField(label='Nombre de la impresion', required=False)
    categorias = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, label='Categorias', choices=CATEGORIAS, required=False)
    precio_min = forms.FloatField(label='Precio Minimo', required=False)
    precio_max = forms.FloatField(label='Precio Maximo', required=False)

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
