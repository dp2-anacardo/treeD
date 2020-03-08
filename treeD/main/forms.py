from django import forms
from main.models import Impresion, Imagen


class ImpresionForm(forms.ModelForm):
    class Meta:
        model = Impresion
        fields = {
            'nombre',
            'descripcion',
            'precio',
            'publicador',
            'categorias',
        }

class CargarImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = [
            'imagen',
        ]
