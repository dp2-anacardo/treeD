
""" Tests del sistema
"""
from django.test import TestCase,Client
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
            'categorias': (9, 11),
            'precio_min': 19.0,
            'precio_max': 21.0
        })
        self.assertQuerysetEqual(response.context['impresiones'], result,transform=lambda x: x)
# Create your tests here.

class crudImpresiones3D(TestCase):
    """ Test referentes al crud de impresiones 3D.
    """
    fixtures = ["initialize.xml"]

    def test_mostrar_impresion_3d(self):
        """ Test que comprueba que el resultado es la impresion de la base de datos.
        """
        result = Impresion.objects.filter(pk=17)
        response = self.client.get('/impresion/mostrarImpresion/17/')
        self.assertEqual(response.context['impresion'],result.first())

    def test_crear_impresion_3d(self):
        """ Test que comprueba el crear de impresion 3d .
        """
        c=Client()
        c.login(username='usuario1', password='usuario1')
        response = c.get('/impresion/crearImpresion/')
        self.assertEqual(response.status_code,200)
        c.logout()

    def test_modificar_impresion_3d(self):
        """ Test que comprueba el modificar de una impresion 3d .
        """
        c=Client()
        c.login(username='usuario1', password='usuario1')
        response = c.get('/impresion/editarImpresion/17/')
        self.assertEqual(response.status_code,200)
        c.logout()

class listarImpresionesTest(TestCase):
    """ Test referentes al listar de impresiones 3D.
    """
    fixtures = ["initialize.xml"]

    def test_listar_impresiones_3d(self):
        """ Test que comprueba que el resultado son todas las impresiones en base de datos.
        """
        result = Impresion.objects.all()

        response = self.client.get('/impresion/listarImpresiones/')
        self.assertEquals(len(response.context['impresiones']),len(result))
        self.assertQuerysetEqual(response.context['impresiones'],result, transform=lambda x: x)
