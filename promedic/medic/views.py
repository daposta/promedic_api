from django.shortcuts import render
from core.models import Responder, ClientProfile
from rest_framework.views import APIView
from django.db.models import Avg, Max, Min,Sum, Count
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MedicRequest
from .serializers import MedicRequestSerializer
from rest_framework import generics, status, views
from newsletters.models import Subscriber



# Create your views here.


class DashboardData_ListView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        #from django.utils import simplejson
        response = []
        responders = Responder.objects.all()
        responder_location_distribution = responders.values('state__name').annotate(total=Count('state__name')).order_by('total')
        responders_kits_distribution = responders.values('kits__name').annotate(total=Count('kits__name')).order_by('total')
        responders_concentration_distribution = responders.values('areas_of_concentration__name').annotate(total=Count('areas_of_concentration__name')).order_by('total')
        
        response.append({'reponders_locations' :responder_location_distribution})
        response.append({'responders_kits': responders_kits_distribution})
        response.append({'responders_concentration': responders_concentration_distribution})
        clients = ClientProfile.objects.all()
        clients_with_diseases = clients.values('diseases__name').annotate(total=Count('diseases__name')).order_by('total')
        clients_with_allergies = clients.values('allergies__name').annotate(total=Count('allergies__name')).order_by('total')
        clients_with_disabilities = clients.values('disabilities__name').annotate(total=Count('disabilities__name')).order_by('total')
        response.append({'clients_with_diseases' :clients_with_diseases})
        response.append({'clients_with_allergies': clients_with_allergies})
        response.append({'clients_with_disabilities': clients_with_disabilities})

        subscriptions = Subscriber.objects.all()
        subscribed = subscriptions.values('unsubscribed').annotate(total=Count('unsubscribed')).order_by('total')#filter(unsubscribed = False)
        #unsubscribed = subscriptions.filter(unsubscribed = True)
        response.append({'subscriptions': subscribed})
        return Response(response)

# def reply_message():
#     ACCOUNT_SID = "AC0e35d1cac079a25d13ce99c5713d81d7"
#     AUTH_TOKEN = "9844935a2bc2b2f61905f616c36cc814"
#
#     client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
#
#     message = client.messages.create(
#         body="Hello Monkey!",
#         to="+12125551234",
#         from_="+19173000189 ",
#     )
#
#     resp = twiml.Response()
#     resp.message(message)

#   http://0.0.0.0:8002/api/medic/medic_request/
def responder(request):
    """Respond to incoming calls with a simple text message."""
    data = request.data
    return Response()


class RequestList(APIView):
    def get(self, request, *args, **kwargs):
        v = request.GET['message']
        return Response({ "message": v})