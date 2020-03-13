from django.test import TestCase, Client
from django.urls import reverse
from main.models import Impresion, Categoria

# Create your tests here.

class listarImpresionesTest(TestCase):
    """ Test referentes al listar de impresiones 3D
    """
    fixtures = ["initialize.xml"]

    def test_listar_impresiones_3d(self):
        """ Test que comprueba que el resultado son todas las impresiones en base de datos
        """
        result = Impresion.objects.all()

        response = self.client.get('/impresion/listarImpresiones/')
        self.assertEquals(len(response.context['impresiones']),len(result))
        self.assertQuerysetEqual(response.context['impresiones'],result, transform=lambda x: x)