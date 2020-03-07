""" Aqui se encuentran los formularios usados por los templates y por views.py
"""

from django import forms
from main.models import Categoria

class BuscadorForm(forms.Form):

    """ Formulario del buscador. Campos:
    - nombre: el buscador busca impresiones que contenga la palabra/s contenidas en 'Nombre'
    - categorias: el buscador busca impresiones que contengan las categorias seleccionadas
    - precio_min: el buscador busca impresiones cuyo precio sea mayor que precio_min
    - precio_max: el buscador busca impresiones cuyo precio sea menor que precio_max
    """
    def validar_precios(self):
        """Valida si esta bien el rango de precio
        """
        cleaned_data = super().clean()
        precio_min = cleaned_data.get("precio_min")
        precio_max = cleaned_data.get("precio_max")

        if precio_min >= precio_max:
            msg = "El precio minimo no puede ser mayor que el precio maximo"
            #self.add_error("precio_min", msg)
            self._errors["precio_min"] = self.error_class([msg])

            del cleaned_data["precio_min"]
            del cleaned_data["precio_max"]

    CATEGORIAS = [(c.idCategoria, c.categoria) for c in Categoria.objects.all()]

    nombre = forms.CharField(label='Nombre de la impresion', required=False)
    categorias = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, label='Categorias', choices=CATEGORIAS, required=False)
    precio_min = forms.FloatField(
        label='Precio Minimo', required=False, validators=[validar_precios])
    precio_max = forms.FloatField(label='Precio Maximo', required=False)
