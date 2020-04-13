"""treeD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from main import views
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', views.buscador_impresiones_3d),
    path('impresion/comprar/<int:pk>/<int:direccion>/', views.comprar_impresion_3d, name="comprarImpresion_url"),
    path('', views.index, name='index'),
    path('misPublicaciones/', views.listar_impresiones_publicadas),
    path('gdpr/', views.gdpr),
    path('impresion/listarVentas/', views.listar_ventas_realizadas, name="listarVentas_url"),
    path('impresion/mostrarImpresion/<int:pk>/', views.mostrar_impresion, name="mostrarImpresion_url"),
    path('impresion/crearImpresion/', views.crear_impresion, name="crearImpresion_url"),
    path('impresion/eliminarImpresion/<int:pk>/', views.eliminar_impresion, name="eliminarImpresion_url"),
    path('impresion/editarImpresion/<int:pk>/', views.editar_impresion, name="editarImpresion_url"),
    path('compra/subirImagenes/<int:pk>/', views.subir_imagenes_prueba_compra, name="subirImagenesPrueba_url"),
    path('paginaError/', views.error, name="error_url"),
    path('editarPerfil/', views.editar_usuario_logueado, name="editarPerfil_url"),
    path('editarPassword/', views.editar_pw_usuario_logueado, name="editarPassword_url"),
    path('mostrarDirecciones/', views.mostrar_direcciones_usuario_logueado, name="editarDirecciones_url"),
    path('añadirDireccion/', views.añadir_direccion_usuario_logueado),
    path('eliminarDireccion/<int:pk>/', views.eliminar_direccion_usuario_logueado, name="eliminarDireccion_url"),
    path('presupuesto/recibidos', views.listar_presupuestos_recibidos, name='presupuestosRecibidos_url'),
    path('presupuesto/enviados', views.listar_presupuestos_enviados, name='presupuestosEnviados_url'),
    path('presupuesto/rechazar/interesado/<int:pk>/', views.rechazar_presupuesto_interesado, name='rechazarPresInteresado_url'),
    path('presupuesto/rechazar/vendedor/<int:pk>/', views.rechazar_presupuesto_vendedor, name='rechazarPresVendedor_url'),
    path('login/', LoginView.as_view(), name="login_url"),
    path('logout/', LogoutView.as_view(), name="logout_url"),
    path('register/', views.crear_usuario, name="crear_usuario_url"),
    path('perfil/<int:pk>/', views.mostrar_perfil, name="mostrarPerfil_url"),
    path('impresion/listarImpresiones/', views.listar_impresiones, name="listarImpresiones_url"),
    path('impresion/listarCompras/', views.listar_compras_impresiones, name="listarComprasRealizas_url"),
    path('usuarios/listar/', views.buscar_usuarios, name="listarPerfiles_url"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('impresion/detalleCompra/<int:pk>/', views.detalles_compra, name="detalleCompra_url"),
    path('presupuesto/detallePresupuesto/<int:pk>/', views.detalles_presupuesto, name="detallePresupuesto_url"),
    path('presupuesto/aceptarPresupuestoInteresado/<int:pk>/', views.aceptar_presupuesto_interesado, name="aceptarPresupuestoInteresado_url"),
    path('presupuesto/comprar/<int:pk>/<int:direccion>/', views.comprar_presupuesto, name="comprarPresupuesto_url"),
    path('presupuesto/mostrarPresupuesto/<int:pk>/', views.mostrarPresupuesto, name="mostrarPresupuesto_url"),
    path('pedirPresupuesto/<int:pk>/', views.pedir_presupuesto, name="pedirPresupuesto_url"),
    path('responderPresupuesto/<int:pk>/', views.responder_presupuesto, name="responderPresupuesto_url"),
    path('hazteAfiliado/', views.hazte_afiliado, name="hazteAfiliado_url"),
    path('usuarios/afiliarse/', views.subscribirse, name="subscripcion_url"),
    path('presupuesto/mostrarRespuesta/<int:pk>/', views.ver_respuesta_presupuesto, name="mostrarRespuesta_url"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

