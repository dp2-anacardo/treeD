from django.test import TestCase, Client
from main.models import Impresion, Compra, Perfil

class BuscadorFormTest(TestCase):
    """ Test referentes al buscador de impresiones 3D.
    """
    fixtures = ["initialize.xml"]

    def test_buscador_impresiones_3d(self):
        """ Test que comprueba que el resultado que coincide con los params
            dados es la del gato gordo
        """
        result = Impresion.objects.filter(pk=18)

        response = self.client.post('/list/', {
            'nombre': 'gato',
            'categorias': (9, 11),
            'precio_min': 19.0,
            'precio_max': 21.0
        })
        self.assertQuerysetEqual(response.context['impresiones'], result, transform=lambda x: x)

class ListarImpresionesPublicadasTest(TestCase):
    """ Test referentes a listar impresiones publicadas
        por un vendedor
    """
    fixtures = ["initialize.xml"]

    def test_listar_impresiones_publicadas_no_logeado(self):
        """ Testea que si no hay usuario logeado retorna al
            index.html
        """
        response = self.client.get('/misPublicaciones/')
        self.assertTemplateUsed(response, 'index.html')

    def test_listar_impresiones_publicadas_usuario(self):
        """ Testea que devuelve las impresiones publicadas
            del vendedor
        """
        self.client.login(username="Ipatia", password="usuario1")
        response = self.client.get('/misPublicaciones/')
        result = Impresion.objects.filter(vendedor=3)
        self.assertQuerysetEqual(response.context['query'], result, transform=lambda x: x)
                
class ListarComprasDeImpresionesTest(TestCase):
    """ Test referentes al listar las compras de las impresiones 3D.
    """
    fixtures = ["initialize.xml"]

    def test_listar_compras_impresiones_3d(self):
        """ Test que comprueba que el resultado son todas las
            compras de impresiones de la base de datos.
        """
        c = Client()
        c.login(username='AAAnuel', password='usuario2')
        response = c.get('/impresion/listarCompras/')
        self.assertEqual(response.status_code, 200)

class CRUDImpresiones3D(TestCase):

    fixtures = ["initialize.xml"]

    def test_mostrar_impresion_3d(self):
        result = Impresion.objects.filter(pk=17)
        response = self.client.get('/impresion/mostrarImpresion/17/')
        self.assertEqual(response.context['impresion'], result.first())

    def test_crear_impresion_3d(self):
        c = Client()
        c.login(username='Ipatia', password='usuario1')
        response = c.get('/impresion/crearImpresion/')
        self.assertEqual(response.status_code, 200)

    def test_modificar_impresion_3d(self):
        c = Client()
        c.login(username='Ipatia', password='usuario1')
        response = c.get('/impresion/editarImpresion/17/')
        self.assertEqual(response.status_code, 200)
    
    def test_eliminar_impresion_3d(self):
        c = Client()
        c.login(username='Ipatia', password='usuario1')
        tamaño_a = len(Impresion.objects.all())
        c.get('/impresion/eliminarImpresion/18/')
        tamaño_d = len(Impresion.objects.all())
        self.assertNotEquals(tamaño_a, tamaño_d)

class ListarImpresionesTest(TestCase):
    """ Test referentes al listar de impresiones 3D.
    """
    fixtures = ["initialize.xml"]

    def test_listar_impresiones_3d(self):
        """ Test que comprueba que el resultado son todas las impresiones en base de datos.
        """
        result = Impresion.objects.all()

        response = self.client.get('/impresion/listarImpresiones/')
        self.assertEquals(len(response.context['impresiones']), len(result))
        self.assertQuerysetEqual(response.context['impresiones'], result, transform=lambda x: x)

class ComprarImpresionesTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_comprar_impresion_comprador(self):
        c = Client()
        c.login(username='AAAnuel', password='usuario2')
        response = c.get('/impresion/comprar/17/')
        self.assertEqual(response.status_code, 200)

    def test_comprar_impresion_vendedor(self):
        c = Client()
        c.login(username='Ipatia', password='usuario1')
        response = c.get('/impresion/comprar/17/')
        self.assertEqual(response.status_code, 302)

    def test_comprar_impresion_inexistente(self):
        c = Client()
        c.login(username='AAAnuel', password='usuario2')
        response = c.get('/impresion/comprar/999/')
        self.assertEqual(response.status_code, 302)

class ListarVentasRealizadas(TestCase):
    """ Test referentes al listar de impresiones vendidas por un vendedor.
    """
    fixtures = ["initialize.xml"]

    def test_listar_ventas_realizadas_no_logeado(self):
        """ Testea que si no hay usuario logeado retorna al
            index.html
        """
        response = self.client.get('/impresion/listarVentas/')
        self.assertTemplateUsed(response, 'index.html')

    def test_listar_ventas_realizadas_vendedor(self):
        """ Testea que devuelve las impresiones vendidas
            del vendedor
        """
        self.client.login(username="Ipatia", password="usuario1")
        response = self.client.get('/impresion/listarVentas/')
        result = Compra.objects.filter(vendedor=3)
        self.assertQuerysetEqual(response.context['query'], result, transform=lambda x: x)

class AdministracionUsuarios(TestCase):

    fixtures = ["initialize.xml"]

    def test_buscar_usuario(self):

        result = Perfil.objects.filter(pk=24)
        self.client.login(username="Ipatia", password="usuario1")
        response = self.client.post('/usuarios/listar/', {
            'nombre': 'luis' })
        response2 = self.client.get('/usuarios/listar/')
        self.assertQuerysetEqual(response.context['query'], result, transform=lambda x: x)
        self.assertEqual(response2.status_code, 200)

