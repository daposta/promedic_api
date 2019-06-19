from .models import Action


def createAction(user, verb, target=None):
   Action(user=user, verb=verb, target=target).save()
