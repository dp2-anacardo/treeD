from django.test import TestCase, Client
from main.models import Impresion

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

    def test_eliminar_imagen(self):
        """ Test que comprueba el modificar de una impresion 3d .
        """
        c=Client()
        c.login(username='usuario1', password='usuario1')
        response = c.get('/impresion/eliminarImagen/20/')
        self.assertEqual(response.status_code,200)
        c.logout()

    def test_añadir_imagen(self):
        """ Test que comprueba el modificar de una impresion 3d .
        """
        c=Client()
        c.login(username='usuario1', password='usuario1')
        response = c.get('/impresion/añadirImagen/17/')
        self.assertEqual(response.status_code,200)
        c.logout()