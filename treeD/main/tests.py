from django.test import TestCase, Client
from main.models import Perfil, DirecPerfil, Compra, ImgPrueba, ImgImpresion, Impresion, Presupuesto, Opinion
from django.contrib.auth.models import User
from pathlib import Path
import os

class OpinionTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_ver_opiniones(self):
        response = self.client.get('/perfil/3/')
        opiniones = Opinion.objects.filter(compra__vendedor__pk=3)
        self.assertQuerysetEqual(
            response.context['opiniones'],
            opiniones, transform=lambda x: x
        )

    def test_crear_opinion_no_valido(self):
        """ Test donde un usuario intenta crear
            una opinion en una compra donde ya
            opino. Redirijido a pagina de error
        """
        self.client.login(username="AAAnuel", password="Usuario2")
        response = self.client.get("/opinion/crearOpinion/25/", follow=True)
        self.assertTemplateUsed(response, "impresiones/paginaError.html")

    def test_crear_opinion_valido(self):
        """ Test donde un usuario intenta crear
            una opinion en una compra.
        """
        self.client.login(username="AAAnuel", password="Usuario2")
        self.client.post("/opinion/crearOpinion/26/", {
            "nota": 3,
            "opinion": "La impresion esta mal hecha, pero el trato ha sido bueno"
        }, follow=True)
        opinion = Opinion.objects.get(compra__pk=26, puntuador__pk=24)
        self.assertEquals(opinion.nota, 3)
        self.assertEquals(
            opinion.opinion,
            "La impresion esta mal hecha, pero el trato ha sido bueno"
        )

class ImgPruebaTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_subir_img_prueba_compra(self):
        """ Miro si esa compra tiene prueba de envio subidas, hago la peticion
            y compruebo que ahora tiene una imagen subida
        """
        self.client.login(username="Ipatia", password="Usuario1")
        file = Path("./main/static/3d.png")
        with open(file, 'rb') as imagen:
            compra = Compra.objects.get(pk=25)
            img_prueba = list(ImgPrueba.objects.filter(compra=compra))
            self.assertTrue(not img_prueba)
            self.client.post("/compra/subirImagenes/25/", {
                "imagen": imagen
            }, follow=True)
            img_prueba = ImgPrueba.objects.get(compra=compra)
            self.assertTrue(img_prueba)
            path = Path("./carga/imagenes/3d.png")
            os.remove(path)


class PedirPresupuestoTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_pedir_presupuesto_no_logueado(self):
        """ Test donde un user no logueado intenta hacer un
            presupuesto. Enviado a la pagina de login
        """
        response = self.client.post('/pedirPresupuesto/3/', {
            'peticion': 'Quiero una figura',
            "descripcion": 'Quiero una figura de IQ del Rainbow Six: Siege'
        }, follow=True)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_pedir_presupuesto_get(self):
        """ Test donde se llama al formulario de pedir presupuesto
        """
        self.client.login(username="AAAnuel", password="Usuario2")
        response = self.client.get('/pedirPresupuesto/3/')
        self.assertTemplateUsed(response, "pedirPresupuesto.html")

    def test_pedir_presupuesto_no_valido(self):
        """ Test donde un user logueado se autopide un presupuesto.
            Enviado a pagina de error
        """
        self.client.login(username="AAAnuel", password="Usuario2")
        response = self.client.post('/pedirPresupuesto/24/', {
            'peticion': 'Quiero una figura',
            "descripcion": 'Quiero una figura de IQ del Rainbow Six: Siege'
        }, follow=True)
        self.assertTemplateUsed(response, "impresiones/paginaError.html")

    def test_pedir_presupuesto_valido(self):
        """ Test donde un user logueado pide un presupuesto. Se
            crea el presupuesto en BD.
        """
        self.client.login(username="AAAnuel", password="Usuario2")
        self.client.post('/pedirPresupuesto/3/', {
            'peticion': 'Quiero una figura 2',
            "descripcion": 'Quiero una figura de IQ del Rainbow Six: Siege'
        }, follow=True)
        presupuesto = Presupuesto.objects.get(peticion='Quiero una figura 2')
        self.assertEqual(
            presupuesto.descripcion,
            'Quiero una figura de IQ del Rainbow Six: Siege'
        )


class ResponderPresupuestoTest(TestCase):

    fixtures = ["initialize.xml"]

    def setUp(self):
        vendedor = Perfil.objects.get(pk=3)
        interesado = Perfil.objects.get(pk=24)
        Presupuesto.objects.create(
            pk=4000,
            interesado=interesado,
            vendedor=vendedor,
            peticion='Quiero una figura',
            descripcion='Quiero una figura de IQ del Rainbow Six: Siege',
            precio=None,
            notas=None,
            fecha_envio=None,
            resp_interesado=None,
            resp_vendedor=None
        )

    def test_responder_presupuesto_no_logueado(self):
        """ Test donde un user no logueado intenta responder un
            presupuesto. Enviado a la pagina de login
        """
        response = self.client.post('/responderPresupuesto/4000/', {
            'notas': 'El tamaño es de 15 cm',
            "fecha_envio": '13/9/2021',
            "precio": 12.0
        }, follow=True)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_responder_presupuesto_get(self):
        """ Test donde se llama al formulario de responder presupuesto
        """
        self.client.login(username="Ipatia", password="Usuario1")
        response = self.client.get('/responderPresupuesto/4000/')
        self.assertTemplateUsed(response, "responderPresupuesto.html")

    def test_responder_presupuesto_no_valido(self):
        """ Test donde un user logueado responde un presupuesto 
            que no le pertenece. Enviado a pagina de error
        """
        self.client.login(username="AAAnuel", password="Usuario2")
        response = self.client.post('/responderPresupuesto/4000/', {
            'notas': 'El tamaño es de 15 cm',
            "fecha_envio": '13/9/2021',
            "precio": 12.0
        }, follow=True)
        self.assertTemplateUsed(response, "impresiones/paginaError.html")

    def test_pedir_presupuesto_valido(self):
        """ Test donde un user logueado responde un presupuesto. Se
            crea el presupuesto en BD.
        """
        self.client.login(username="Ipatia", password="Usuario1")
        self.client.post('/responderPresupuesto/4000/', {
            'notas': 'El tamaño es de 15 cm',
            "fecha_envio": '13/9/2021',
            "precio": 12.0
        }, follow=True)
        presupuesto = Presupuesto.objects.get(pk=4000)
        self.assertEqual(presupuesto.precio, 12.0)


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
        self.assertQuerysetEqual(
            response.context['impresiones'], result, transform=lambda x: x)


class EditarPerfilTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_editar_perfil_valido(self):
        """ Los campos son validos, redirige al index y ahora esta el user editado """

        self.client.login(username="Ipatia", password="Usuario1")
        response = self.client.post('/editarPerfil/', {
            'username': 'ManuErCaximba',
            "nombre": 'Manuel',
            "apellidos": "Roldan",
            "descripcion": "Hola soy ManuErCaximba",
            "email": "caximba@gmail.com"
        }, follow=True)
        perfil_actualizado = Perfil.objects.get(nombre="Manuel")
        self.assertEquals(perfil_actualizado.usuario.username, "ManuErCaximba")

    def test_editar_perfil_no_valido(self):
        """ Los campos no son validos, vuelve al formulario """

        self.client.login(username="Ipatia", password="Usuario1")
        response = self.client.post('/editarPerfil/', {
            'username': '<<<<<<',
            "nombre": 'Manuel',
            "apellidos": "Roldan",
            "descripcion": "Hola soy ManuErCaximba",
            "email": "caximba@gmail.com"
        }, follow=True)
        self.assertTemplateUsed(response, 'editarPerfil.html')

    def test_editar_password_no_valido(self):
        """ La contraseña no es valida, vuelve al formulario """

        self.client.login(username="Ipatia", password="Usuario1")
        response = self.client.post('/editarPassword/', {
            'password': 'Usuario2',
            "check_pw": 'gggggggg',
        }, follow=True)
        self.assertTemplateUsed(response, 'editarPassword.html')

    def test_editar_password_valido(self):
        """ La contraseña es valida, retorna al index y ahora la pass es otra """

        self.client.login(username="Ipatia", password="Usuario1")
        response = self.client.post('/editarPassword/', {
            'password': 'Usuario2',
            "check_pw": 'Usuario2',
        }, follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.client.logout()
        self.client.login(username="Ipatia", password="Usuario2")
        user = User.objects.get(username="Ipatia")
        self.assertTrue(user.is_authenticated)

    def test_mostrar_direcciones(self):

        self.client.login(username="Ipatia", password="Usuario1")
        user = User.objects.get(username="Ipatia")
        perfil = Perfil.objects.get(usuario=user)
        response = self.client.get('/mostrarDirecciones/')
        direcciones = DirecPerfil.objects.filter(perfil=perfil)
        self.assertQuerysetEqual(
            response.context['direcciones'], direcciones, transform=lambda x: x)

    def test_añadir_eliminar_direccion(self):
        """ Creamos una direccion, testeamos que se ha creado, la borramos y comprobamos que se ha borrado """

        """ Añadir direccion """
        self.client.login(username="Ipatia", password="Usuario1")
        user = User.objects.get(username="Ipatia")
        perfil = Perfil.objects.get(usuario=user)
        response = self.client.post('/añadirDireccion/', {
            'ciudad': 'Sevilla',
            'localidad': 'Sevilla',
            'calle': 'C/Anacardo',
            'numero': 'Segundo piso de pistacho',
            'codigo_postal': '41001',
        }, follow=True)
        direccion_added = DirecPerfil.objects.get(
            calle='C/Anacardo')
        self.assertTemplateUsed(response, 'mostrarDirecciones.html')
        self.assertEquals(direccion_added.calle,
                          'C/Anacardo')
        self.assertEquals(direccion_added.perfil, perfil)

        """ Eliminar direccion """
        response = self.client.get(
            '/eliminarDireccion/' + str(direccion_added.id) + '/')
        direccion = list(DirecPerfil.objects.filter(
            calle='C/Anacardo'))
        self.assertTrue(not direccion)


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
        self.assertRedirects(response, '/login/?next=/misPublicaciones/')

    def test_listar_impresiones_publicadas_usuario(self):
        """ Testea que devuelve las impresiones publicadas
            del vendedor
        """
        self.client.login(username="Ipatia", password="Usuario1")
        response = self.client.get('/misPublicaciones/')
        result = Impresion.objects.filter(vendedor=3)
        self.assertQuerysetEqual(
            response.context['query'], result, transform=lambda x: x)


class ListarComprasDeImpresionesTest(TestCase):
    """ Test referentes al listar las compras de las impresiones 3D.
    """
    fixtures = ["initialize.xml"]

    def test_listar_compras_impresiones_3d(self):
        """ Test que comprueba que el resultado son todas las
            compras de impresiones de la base de datos.
        """
        c = Client()
        c.login(username='AAAnuel', password='Usuario2')
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
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/impresion/crearImpresion/')
        self.assertEqual(response.status_code, 200)

    def test_modificar_impresion_3d(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/impresion/editarImpresion/17/')
        self.assertEqual(response.status_code, 200)

    def test_eliminar_impresion_3d(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
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
        self.assertQuerysetEqual(
            response.context['impresiones'], result, transform=lambda x: x)


class ComprarImpresionesTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_comprar_impresion_comprador(self):
        c = Client()
        c.login(username='AAAnuel', password='Usuario2')
        response = c.get('/impresion/comprar/17/31/')
        self.assertEqual(response.status_code, 200)

    def test_comprar_impresion_vendedor(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/impresion/comprar/17/31/')
        self.assertEqual(response.status_code, 302)

    def test_comprar_impresion_inexistente(self):
        c = Client()
        c.login(username='AAAnuel', password='Usuario2')
        response = c.get('/impresion/comprar/0/31/')
        self.assertEqual(response.status_code, 302)

    def test_factura_pago_impresion(self):
        c = Client()
        c.login(username='AAAnuel', password='Usuario2')
        response1 = c.get('/impresion/detalleCompra/17/')
        response2 = self.client.post('/impresion/detalleCompra/17/')

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 302)


class ListarVentasRealizadas(TestCase):
    """ Test referentes al listar de impresiones vendidas por un vendedor.
    """
    fixtures = ["initialize.xml"]

    def test_listar_ventas_realizadas_no_logeado(self):
        """ Testea que si no hay usuario logeado retorna al
            index.html
        """
        response = self.client.get('/impresion/listarVentas/')
        self.assertRedirects(response, '/login/?next=/impresion/listarVentas/')

    def test_listar_ventas_realizadas_vendedor(self):
        """ Testea que devuelve las impresiones vendidas
            del vendedor
        """
        self.client.login(username="Ipatia", password="Usuario1")
        response = self.client.get('/impresion/listarVentas/')
        result = Compra.objects.filter(vendedor=3)
        self.assertQuerysetEqual(
            response.context['query'], result, transform=lambda x: x)


class AdministracionUsuarios(TestCase):

    fixtures = ["initialize.xml"]

    def test_buscar_usuario(self):

        result = Perfil.objects.filter(pk=3)
        self.client.login(username="AAAnuel", password="Usuario2")
        response = self.client.post('/usuarios/listar/', {
            'nombre': 'Ipatia'})
        response2 = self.client.get('/usuarios/listar/')
        self.assertQuerysetEqual(
            response.context['query'], result, transform=lambda x: x)
        self.assertEqual(response2.status_code, 200)

    def test_listar_usuarios(self):

        self.client.login(username="Ipatia", password="Usuario1")
        response = self.client.get('/usuarios/listar/')
        self.assertEqual(response.status_code, 200)


class RegistroTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_registro(self):
        c = Client()
        response = c.get('/register/')
        self.assertEqual(response.status_code, 200)


class VerPerfilTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_ver_perfil(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/perfil/24/')
        self.assertEqual(response.status_code, 200)

    def test_ver_perfil_inexistente(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/perfil/0/')
        self.assertEqual(response.status_code, 302)


class ListarPresupuestosTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_listar_presupuestos_interesados(self):
        c = Client()
        c.login(username='AAAnuel', password='Usuario2')
        response = c.get('/presupuesto/enviados/')

        presupuestos_enviados = Presupuesto.objects.all().filter(interesado=24)

        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            len(response.context['presupuestos']), len(presupuestos_enviados))

    def test_listar_presupuestos_vendedores(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/presupuesto/recibidos/')

        presupuestos_recibidos = Presupuesto.objects.all().filter(vendedor=3)

        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            len(response.context['presupuestos']), len(presupuestos_recibidos))


class RechazarPresupuestosTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_rechazar_presupuesto_vendedor(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/presupuesto/rechazar/vendedor/34/')
        self.assertEqual(response.status_code, 200)

    def test_rechazar_presupuesto_vendedor_aceptado(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/presupuesto/rechazar/vendedor/32/')
        self.assertEqual(response.status_code, 302)

    def test_rechazar_presupuesto_vendedor_rechazado(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/presupuesto/rechazar/vendedor/33/')
        self.assertEqual(response.status_code, 302)

    def test_rechazar_presupuesto_interesado(self):
        c = Client()
        c.login(username='AAAnuel', password='Usuario2')
        response = c.get('/presupuesto/rechazar/interesado/32/')
        self.assertEqual(response.status_code, 200)

    def test_rechazar_presupuesto_interesado_aceptado(self):
        c = Client()
        c.login(username='AAAnuel', password='Usuario2')
        response = c.get('/presupuesto/rechazar/interesado/35/')
        self.assertEqual(response.status_code, 302)

    def test_rechazar_presupuesto_interesado_rechazado(self):
        c = Client()
        c.login(username='AAAnuel', password='Usuario2')
        response = c.get('/presupuesto/rechazar/interesado/33/')
        self.assertEqual(response.status_code, 302)

    def test_rechazar_presupuesto_no_recibido(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/presupuesto/rechazar/vendedor/35')
        self.assertEqual(response.status_code, 301)

    def test_rechazar_presupuesto_no_enviado(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/presupuesto/rechazar/interesado/32')
        self.assertEqual(response.status_code, 301)


class AceptarPresupuestosTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_aceptar_presupuesto_vendedor(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/presupuesto/aceptarPresupuestoVendedor/32/')
        presupuesto = Presupuesto.objects.get(pk=32)
        self.assertEqual(presupuesto.resp_vendedor, True)

    def test_aceptar_presupuesto_interesado(self):
        c = Client()
        c.login(username='AAAnuel', password='Usuario2')
        response = c.get('/presupuesto/aceptarPresupuestoInteresado/32/')
        presupuesto = Presupuesto.objects.get(pk=32)
        usuario = Perfil.objects.get(pk=24)
        self.assertEqual(presupuesto.interesado, usuario)

    def test_aceptar_presupuesto_interesado_invalido(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/presupuesto/aceptarPresupuestoInteresado/32/')
        presupuesto = Presupuesto.objects.get(pk=32)
        usuario = Perfil.objects.get(pk=3)
        self.assertNotEqual(presupuesto.interesado, usuario)

    def test_factura_pago_presupuesto(self):
        c = Client()
        c.login(username='AAAnuel', password='Usuario2')
        response1 = c.get('/presupuesto/detallePresupuesto/32/')
        response2 = self.client.post('/impresion/detalleCompra/32/')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 302)

    def test_factura_pago_presupuesto_invalido(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response1 = c.get('/presupuesto/detallePresupuesto/32/')
        self.assertEqual(response1.status_code, 302)

    def test_comprar_presupuesto_interesado(self):
        c = Client()
        c.login(username='AAAnuel', password='Usuario2')
        response = c.get('/presupuesto/comprar/32/31/')
        self.assertEqual(response.status_code, 200)

    def test_comprar_presupuesto_vendedor(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/impresion/comprar/32/31/')
        self.assertEqual(response.status_code, 302)


class VerPresupuestoTest(TestCase):

    fixtures = ["initialize.xml"]

    def test_ver_presupuesto(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/presupuesto/mostrarPresupuesto/32/')
        self.assertEqual(response.status_code, 200)

    def test_ver_presupuesto_invalido(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/presupuesto/mostrarPresupuesto/0/')
        self.assertEqual(response.status_code, 302)


class Subscripciones(TestCase):

    fixtures = ["initialize.xml"]

    def test_subscripcion_correcta(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/usuarios/afiliarse/')
        self.assertEqual(response.status_code, 200)

    def test_subscripcion_incorrecta(self):
        c = Client()
        c.login(username='Ipatia', password='suario1')
        response = c.get('/usuarios/afiliarse/')
        self.assertEqual(response.status_code, 302)

class EstadisticasVenta(TestCase):

    fixtures = ["initialize.xml"]

    def test_estadisticas_afiliado(self):
        c = Client()
        c.login(username='Ipatia', password='Usuario1')
        response = c.get('/usuarios/estadisticas/')
        self.assertEqual(response.status_code, 200)
