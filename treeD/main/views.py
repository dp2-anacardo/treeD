from django.shortcuts import render
from main.models import Perfil, Impresion

# Create your views here.

def index(request):
    return render(request, 'index.html',)

def listar_impresiones_publicadas(request):
    """
    Funcion que lista las impresiones publicadas por un vendedor
    """
    if request.user.is_authenticated:
        perfil_user = Perfil.objects.get(usuario=request.user)
        query = Impresion.objects.filter(publicador=perfil_user)
        return render(request, "list2.html", {"query": query})

    return render(request, 'index.html')
