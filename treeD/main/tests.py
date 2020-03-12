""" Tests del sistema
"""
from django.test import TestCase
from main.models import Impresion

class BuscadorFormTest(TestCase):
    """ Test referentes al buscador de impresiones 3D
    """
    fixtures = ["initialize.xml"]
    def test_buscador_impresiones_3d(self):
        """ Test que comprueba que el resultado que coincide con los params
            dados es la impresion 2
        """
        result = Impresion.objects.filter(pk=18)

        response = self.client.post('/list/', {
            'nombre': 'impresion',
            'categorias': ('9', '11'),
            'precio_min': 19.0,
            'precio_max': 21.0
        })
        self.assertEqual(response.context['query'].first(), result.first())
