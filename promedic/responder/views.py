from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from core.models import *
from  .serializers import *
from django.contrib.auth import authenticate, login,logout
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

import datetime
# Create your views here.


# Create your views here.
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': SystemUserSerializer(user).data
    }


class LoginView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)
        mobile = data.get('mobile', None)
        password = data.get('password', None)
        account = None
        if mobile and password:
            account = authenticate(mobile=mobile, password=password)
            if account is not None:
                if account.is_active:
                    if request.user.user_type and request.user.user_type == 'RES':
                        login(request,account)
                        serialized = SystemUserSerializer(account)
                        return Response(serialized.data)
                    else:
                        return Response({'status': 'Unauthorized',  'message': 'Account not a responder.'}
                        , status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({'status': 'Unauthorized',  'message': 'This account has been disabled.'}
                        , status=status.HTTP_401_UNAUTHORIZED)

            else:
                return Response({'status': 'Unauthorized',  'message': 'Please provide valid login credentials.'}
                        , status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'Unauthorized',  'message': 'Please provide an email and password.'}
                        , status=status.HTTP_401_UNAUTHORIZED)



class LogoutView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response({}, status = status.HTTP_204_NO_CONTENT)


from django.core import serializers
from django.http import HttpResponse

class CurrentProfile(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    


    def get(self, request, *args, **kwargs):
        data, response = None, None
        try:
            data = Responder.objects.get(member = request.user)
        except Exception as e:
            pass
        if data:
            response = ResponderDetailSerializer(data)
            return Response(response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


    # def patch(self, request):
    #     new_data = { 'client': request.user.id, 'first_name': request.data['first_name'], 'last_name': request.data['last_name'], 
    #     'middle_name': request.data['middle_name'] if 'middle_name' in request.data else '',
    #     'contact_address': request.data['contact_address'], 'genotype' : request.data['genotype'], 'blood_group': request.data['blood_group'],
    #     'nick_name': request.data['nick_name'], 'gender': request.data['gender'], 'emergency_name': request.data['emergency_name'],
    #     'emergency_number' : request.data['emergency_number'], 'allergies': request.data['allergies_list'] if 'allergies_list' in request.data else [],
    #     'diseases': request.data['diseases_list'] if 'diseases_list' in request.data else [],
    #     'disabilities': request.data['disabilities_list'] if 'disabilities_list' in request.data else [], 
    #     'date_of_birth': request.data['date_of_birth'], 'nhis_number': request.data['nhis_number'] if 'nhis_number' in request.data else '',
    #     'hmo': request.data['hmo'],
    #     }
    #     profile = Responder.objects.get(client = request.user)
    #     serializer = ResponderSerializer(profile, data=new_data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
