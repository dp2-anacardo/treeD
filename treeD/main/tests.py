from django.test import TestCase, Client
from django.urls import reverse
from main.models import Impresion, Categoria
from django.contrib.auth.models import User

# Create your tests here.

class listarComprasDeImpresionesTest(TestCase):
    """ Test referentes al listar las compras de las impresiones 3D
    """
    fixtures = ["initialize.xml"]

    def test_listar_compras_impresiones_3d(self):
        """ Test que comprueba que el resultado son todas las compras de impresiones de la base de datos
        """
        c=Client()
        c.login(username='usuario2', password='usuario2')
        response = c.get('/impresion/listarCompras/')
        self.assertEqual(response.status_code,200)
        c.logout()