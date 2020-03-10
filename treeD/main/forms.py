from django import forms
from main.models import Impresion, Imagen
from django.core.exceptions import ValidationError


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
