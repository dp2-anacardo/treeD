from django.test import TestCase
from main.models import Impresion

# Create your tests here.
class ListarImpresionesPublicadasTest(TestCase):
    """ Test referentes a listar impresiones publicadas
        por un vendedor
    """
    fixtures = ["initialize.xml"]

    def test_listar_impresiones_publicadas_no_logeado(self):
        """ Testea que si no hay usuario logeado retorna al
            index.html
        """
        response = self.client.get('/list2/')
        self.assertTemplateUsed(response, 'index.html')

    def test_listar_impresiones_publicadas_usuario(self):
        """ Testea que devuelve las impresiones publicadas
            del vendedor
        """
        self.client.login(username="usuario1", password="usuario1")
        response = self.client.get('/list2/')
        result = Impresion.objects.filter(publicador=3)
        self.assertQuerysetEqual(response.context['query'], result, transform=lambda x: x)
