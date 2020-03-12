from django.test import TestCase, Client
from django.urls import reverse
from main.models import Impresion

# Create your tests here.

class listarImpresionesTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.listarImpresiones_url = reverse('listarImpresiones_url')


    def listarImpresiones_GET(self):

        response = self.client.get(self.listarImpresiones_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'impresiones/listarImpresiones.html')