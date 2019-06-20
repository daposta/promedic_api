from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from core.models import *
from  client.serializers import *
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

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user).data
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
                    if request.user.user_type and request.user.user_type == 'CL':
                        login(request,account)
                        serialized = UserSerializer(account)
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


from newsletters.models import Subscriber
def create_newsletter_subscriber(email):
    try:
        Subscriber.objects.create(email = email)
    except Exception as e:
        pass
    
from authy.api import AuthyApiClient

AUTHY_API_KEY ='lkw3UkxH2bWFa60ahEJTVebPHgYKwQHc'
authy_api = AuthyApiClient(AUTHY_API_KEY)

def verify_number(mobile):
    g = authy_api.phones.verification_start(mobile, 234, via='sms')
    return g


from django.contrib.auth.hashers import make_password

class CreateUserView(CreateAPIView):

    model = Member.objects.all() 
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


    def create(self, request, *args, **kwargs):
        new_data = {'mobile': request.data['mobile'].strip(), 'email': request.data['email'] if 'email' in request.data else '', 
        'password': make_password(request.data['password']),
        'user_type': 'CL'}
        if Member.objects.filter(mobile = new_data['mobile']):
            return Response({ 'message': 'User with mobile already exists.'}
                        , status=status.HTTP_400_BAD_REQUEST)
        if Member.objects.filter(email = new_data['email']):
            return Response({ 'message': 'User with email already exists.'}
                        , status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data= new_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response( e)
            if 'email' in new_data:
                create_newsletter_subscriber(new_data['email'])
                verify_number(new_data['mobile'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllergyList(generics.ListCreateAPIView):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)



class DisablityList(generics.ListCreateAPIView):
    queryset = Disablity.objects.all()
    serializer_class = DisablitySerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
		


class GenderList(generics.ListCreateAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)



class GenotypeList(generics.ListCreateAPIView):
    queryset = Genotype.objects.all()
    serializer_class = GenotypeSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)



class BloodGroupList(generics.ListCreateAPIView):
    queryset = BloodGroup.objects.all()
    serializer_class = BloodGroupSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class HMOList(generics.ListCreateAPIView):
    queryset = HMO.objects.all()
    serializer_class = HMOSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class DiseaseList(generics.ListCreateAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)



def convertDate(d):
    v = datetime.datetime.strptime(d, '%d/%m/%Y').strftime('%Y-%m-%d')
    return v

class CreateProfileView(CreateAPIView):

    model = ClientProfile.objects.all()
    permission_classes = [
        IsAuthenticated # Or anon users can't register
    ]
    serializer_class = ClientProfileSerializer
    authentication_classes = (JSONWebTokenAuthentication,)


    def create(self, request, *args, **kwargs):
        new_data = {'client': request.user.id, 'first_name': request.data['fName'], 'last_name': request.data['lastName'], 
        'middle_name': request.data['middleName'] if 'middleName' in request.data else '', 'status': 'V',
        'contact_address': request.data['address'], 'genotype' : request.data['genotype'], 'blood_group': request.data['bloodGrp'],
        'nick_name': request.data['nickName'] if 'nickName' in request.data else '', 'gender': request.data['gender'], 
        'emergency_name': request.data['contactName'],
        'emergency_number' : request.data['contactNo'], 'allergies': request.data['allergies'] if 'allergies' in request.data else [],
        'diseases': request.data['diseases'] if 'diseases' in request.data else [],
        'disabilities': request.data['disabilities'] if 'disabilities' in request.data else [], 
        'date_of_birth': request.data['dob'], 'nhis_number': request.data['nhis_number'] if 'nhis_number' in request.data else '', 
        'hmo': request.data['hmo'] if 'hmo' in request.data else None,


        }
        serializer = ClientProfileSerializer(data= new_data)
        if serializer.is_valid():
            instance = None
            try:
                serializer.save()
            except Exception as e:
                return  Response( e)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.core import serializers
from django.http import HttpResponse
class CurrentProfile(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    


    def get(self, request, *args, **kwargs):
        data, response = None, None
        try:
            data = ClientProfile.objects.get(client = request.user)
        except Exception as e:
            pass
        if data:
            response = ExClientProfileSerializer(data)
            return Response(response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


    def patch(self, request):
        new_data = { 'client': request.user.id, 'first_name': request.data['first_name'], 'last_name': request.data['last_name'], 
        'middle_name': request.data['middle_name'] if 'middle_name' in request.data else '',
        'contact_address': request.data['contact_address'], 'genotype' : request.data['genotype'], 
        'blood_group': request.data['blood_group'],
        'nick_name': request.data['nick_name'], 'gender': request.data['gender'], 'emergency_name': request.data['emergency_name'],
        'emergency_number' : request.data['emergency_number'], 'allergies': request.data['allergies_list'] if 'allergies_list' in request.data else [],
        'diseases': request.data['diseases_list'] if 'diseases_list' in request.data else [],
        'disabilities': request.data['disabilities_list'] if 'disabilities_list' in request.data else [], 
        'date_of_birth': request.data['date_of_birth'], 'nhis_number': request.data['nhis_number'] if 'nhis_number' in request.data else '',
        'hmo': request.data['hmo'],
        }
        profile = ClientProfile.objects.get(client = request.user)
        serializer = ClientProfileSerializer(profile, data=new_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator  

def send_reset_link(x, msg):
    '''check if user with number has a email'''
    from django.core.mail import send_mail
    
    send_mail('PROMedic Password Reset', msg, 'Reset @ PROMedic<bonjour@levilabs.com>',
     [x], fail_silently=False)


def compose_reset_email(client):
    uid = urlsafe_base64_encode(force_bytes(client.client.pk))
    token =  default_token_generator.make_token(client.client)
    try:
        store_reset_info(client, uid, token)
    except Exception as e:
        return Response(e)
    
    
    var_dict = {
        'domain_name' : 'http://promedic.com.ng/', #'http://localhost:4200/',
        'rest_link' : ('#/reset/' + token  + '/' + uid),
        'first_name': client.first_name
    }
    email_msg = ''' 
        Hi {first_name},
        You're receiving this email because you requested a password reset for your user account at
        PROMedic .
        Please go to the following page and choose a new password:

         {domain_name}{rest_link}

    '''.format(**var_dict)
    return email_msg


def store_reset_info(client, uid, token):
    expiry_date = datetime.date.today() + datetime.timedelta(days=5)
    if PasswordReset.objects.filter(client = client.client):
        PasswordReset.objects.filter(client = client.client).delete()
        PasswordReset.objects.create(client = client.client, token = token, expiry =  expiry_date)
    else:
        PasswordReset.objects.create(client = client.client, token = token, expiry =  expiry_date)
    
    

class ForgotPassword(APIView):

    def post(self, request, format=None):
        data, response = None, None
        try:
            data = ClientProfile.objects.get(client__email = request.data['email'], client__user_type='CL')
        except Exception as e:
            return Response({ 'message': 'User with email does not exist.'}
                        , status=status.HTTP_400_BAD_REQUEST)
        if data:
            msg = compose_reset_email(data)
            send_reset_link(request.data['email'], msg)
            return Response(status=status.HTTP_200_OK)





from django.contrib.auth import get_user_model


class ResetPassword(APIView):
    

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        UserModel = get_user_model()
        try:
            uid = urlsafe_base64_decode(request.data['params']['uid'])
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        token = request.data['params']['token']
        if user is not None and PasswordReset.objects.get(client = user, token = token ):
            user.password = make_password(request.data['password'])
            user.save()
            PasswordReset.objects.get(client = user, token = token ).delete()

        return Response(status=status.HTTP_200_OK)
        



class ActivateUser(APIView):
    

    def post(self, request, format=None):
        token = request.data['token'] if 'token' in request.data else ''
        mobile = request.data['mobile'] if 'mobile' in request.data else ''
        country = 234
        # authy_api = AuthyApiClient(AUTHY_API_KEY)
        verified = authy_api.phones.verification_check(mobile, country, token)
        if verified.ok():
            user= None
            try:
                user = Member.objects.get(mobile  = request.data['mobile'])
            except Exception as e:
                return Response( e)
            if user:
                user.is_active=True
                user.save()
        else:
            return Response({ 'message': 'Token does not match mobile number.'}
                        , status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)



class NewsletterUnsubscribeView(APIView):
    

    def post(self, request, format=None):
        if 'email' in request.data:
            subscriber = None
            try:
                subscriber = Subscriber.objects.get(email = request.data['email'])
            except Exception as e:
                return Response({ 'message': 'Email does not exist for newsletters.'}
                        , status=status.HTTP_400_BAD_REQUEST)
            if subscriber:
                subscriber.unsubscribed = True
                subscriber.save()
            
                return Response(status=status.HTTP_200_OK)
        else:
            return Response({ 'message': 'Please submit email.'}
                        , status=status.HTTP_400_BAD_REQUEST)


