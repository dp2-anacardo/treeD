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
from main import views
from main.views import mostrarImpresion, mostrarTodasMisImpresiones,crearImpresion,editarImpresion,eliminarImpresion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('impresion/mostrarImpresion/<idImpresion>/', views.mostrarImpresion, name="mostrarImpresion_url"),
    path('impresion/listarImpresiones/', views.mostrarTodasMisImpresiones, name="mostrarTodasMisImpresiones_url"),
    path('impresion/crearImpresion/', views.crearImpresion, name="crearImpresion_url"),
    path('impresion/crearImpresion/<idImpresion>/', views.editarImpresion, name="editarImpresion_url"),
    path('impresion/eliminarImpresion/<idImpresion>/', views.eliminarImpresion, name="eliminarImpresion_url"),
]
