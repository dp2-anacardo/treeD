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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', views.buscador_impresiones_3d),
    path('impresion/comprar/<int:pk>/', views.comprar_impresion_3d, name="comprarImpresion_url"),
    path('', views.index, name='index'),
    path('misPublicaciones/', views.listar_impresiones_publicadas),
    path('impresion/listarVentas/', views.listar_ventas_realizadas, name="listarVentas_url"),
    path('impresion/mostrarImpresion/<int:pk>/', views.mostrar_impresion, name="mostrarImpresion_url"),
    path('impresion/crearImpresion/', views.crear_impresion, name="crearImpresion_url"),
    path('impresion/eliminarImpresion/<int:pk>/', views.eliminar_impresion, name="eliminarImpresion_url"),
    path('impresion/editarImpresion/<int:pk>/', views.editar_impresion, name="editarImpresion_url"),
    path('compra/subirImagenes/<int:pk>/', views.subir_imagenes_prueba_compra, name="subirImagenesPrueba_url"),
    path('paginaError/', views.error, name="error_url"),
    path('login/', LoginView.as_view(), name="login_url"),
    path('logout/', LogoutView.as_view(), name="logout_url"),
    path('impresion/listarImpresiones/', views.listar_impresiones, name="listarImpresiones_url"),
    path('impresion/listarCompras/', views.listar_compras_impresiones, name="listarComprasRealizas_url"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

