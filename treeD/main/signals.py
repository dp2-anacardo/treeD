from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.contrib.auth.models import User
from main.models import Perfil

@receiver(valid_ipn_received)
def ipn_receiver(sender, **kwargs):

    ipn_obj = sender
    if (ipn_obj.txn_type == "subscr_cancel") or (ipn_obj.txn_type == "subscr_failed"):
        id = ipn_obj.custom
        usuario = Perfil.objects.get(id=id)
        usuario.es_afiliado = False
        usuario.save()
    else:
        pass
valid_ipn_received.connect(ipn_receiver)