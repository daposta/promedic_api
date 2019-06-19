# Create your views here.
from django.shortcuts import render_to_response
import json
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from django.db.models import Q
from rest_framework import permissions
from django.contrib.auth import authenticate, login,logout
from rest_framework import generics, status, views
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from  .serializers import *
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .utils import generate_responder_serial
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from django.conf import settings
import os
from django.db.models import Q
#from rest_framework.authentication import (BaseJSONWebTokenAuthentication)


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
                    if request.user.user_type and request.user.user_type == 'SU':
                        login(request,account)
                        serialized = SystemUserSerializer(account)
                        return Response(serialized.data)
                    else:
                        return Response({'status': 'Unauthorized',  'message': 'Account not an admin.'}
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




# class CustomJSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):

#     def authenticate_credentials(self, payload):
#         """
#         Returns an active user that matches the payload's user id and email.
#         """
#         print 'booya'
#         User = get_user_model()
#         username = jwt_get_username_from_payload(payload)
#         print 'user....', username


#         if not username:
#             msg = _('Invalid payload.')
#             raise exceptions.AuthenticationFailed(msg)

#         try:
#             user = User.objects.get_by_natural_key(username)
#         except User.DoesNotExist:
#             msg = _('Invalid signature.')
#             raise exceptions.AuthenticationFailed(msg)

#         if not user.is_active:
#             msg = _('User account is disabled.')
#             raise exceptions.AuthenticationFailed(msg)

#         return user


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class HMOList(generics.ListCreateAPIView):
    queryset = HMO.objects.all()
    serializer_class = HMOSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'hmo' in self.request.query_params:
            search = self.request.query_params['hmo']
            if search:
                return HMO.objects.filter(name__icontains =  search.strip())
        return HMO.objects.all()


    def create(self, request, *args, **kwargs):
        new_data = {'name': request.data['name'].strip(), 'address': request.data['address'], 
         'state': request.data['state'], 'mobile1': request.data['mobile1'],
        'mobile2': request.data['mobile2'], }
        if HMO.objects.filter(name = request.data['name'].strip()):
            raise serializers.ValidationError('HMO name already exists')
        serializer = HMOSerializer(data=new_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response( e)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'status' : 'Bad request',
            'message': 'HMO could not be created with received data.',
            'errors' : serializer.errors # for example
            }, status=status.HTTP_400_BAD_REQUEST)



class HMODetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HMO.objects.all()
    serializer_class = HMODetailSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.name =  request.data['name']
        instance.address = request.data['address']
        instance.mobile1 = request.data['mobile1']
        instance.mobile2 = request.data['mobile2']
        if  request.data['state']:
            instance.state = State.objects.get(pk = request.data['myState'])
        
        try:
            instance.save()
        except Exception as e:
            return Response( e)
        
        return Response(status=status.HTTP_200_OK)


class StateList(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'state' in self.request.query_params:
            search = self.request.query_params['state']
            if search:
                return State.objects.filter(name__icontains =  search.strip())
        return State.objects.all()



class StateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class StateListSelect(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class LocalGovernmentList(generics.ListCreateAPIView):
    queryset = LocalGovernment.objects.all()
    serializer_class = LocalGovernmentDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'lg' in self.request.query_params:
            search = self.request.query_params['lg'].strip()
            if search:
                return LocalGovernment.objects.filter(Q(name__icontains =  search) |Q(state__name__icontains= search)).select_related( 
                'state' ).prefetch_related( 
                )

        return LocalGovernment.objects.all().select_related(
                'state' ).prefetch_related( 
                )



class LGADetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocalGovernment.objects.all()
    serializer_class = LocalGovernmentDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.name =  request.data['name']
        if  request.data['state']:
            instance.state = State.objects.get(pk = request.data['myState'])
        
        try:
            instance.save()
        except Exception as e:
            return Reponse(e)
        
        return Response(status=status.HTTP_200_OK)


    

class LocalGovernmentListFilter(generics.ListCreateAPIView):
    queryset = LocalGovernment.objects.all()
    serializer_class = LocalGovernmentSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        return LocalGovernment.objects.filter(state__pk=  self.request.query_params['state'])




class DocumentTypeList(generics.ListCreateAPIView):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
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

    

class BloodTypeList(generics.ListCreateAPIView):
    queryset = BloodType.objects.all()
    serializer_class = BloodTypeSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

# class DiseaseList(generics.ListCreateAPIView):
#     queryset = Disease.objects.all()
#     serializer_class = DiseaseSerializer
#     authentication_classes = (JSONWebTokenAuthentication,)
#     permission_classes = (IsAuthenticated,)



class DrugSideEffectList(generics.ListCreateAPIView):
    queryset = DrugSideEffect.objects.all()
    serializer_class = DrugSideEffectSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class DrugClassificationList(generics.ListCreateAPIView):
    queryset = DrugClassification.objects.all()
    serializer_class = DrugClassificationSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class DrugBrandList(generics.ListCreateAPIView):
    queryset = DrugBrand.objects.all()
    serializer_class = DrugBrandSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class DrugFormList(generics.ListCreateAPIView):
    queryset = DrugForm.objects.all()
    serializer_class = DrugFormSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class DrugDispenseTypeList(generics.ListCreateAPIView):
    queryset = DrugDispenseType.objects.all()
    serializer_class = DrugDispenseTypeSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class DrugIndicationList(generics.ListCreateAPIView):
    queryset = DrugIndication.objects.all()
    serializer_class =DrugIndicationSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class DrugContraIndicationList(generics.ListCreateAPIView):
    queryset = DrugContraIndication.objects.all()
    serializer_class = DrugContraIndicationSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
class DrugList(generics.ListCreateAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'drug' in self.request.query_params:
            search = self.request.query_params['drug']
            if search:
                return Drug.objects.filter(name__icontains =  search.strip())
        return Drug.objects.all()


    def create(self, request, *args, **kwargs):
        new_data = {'name': request.data['name'].strip(), 'brand': request.data['brand'], 
        'form': request.data['form'], 'dispense_type': request.data['dispense_type'], 'classifications': request.data['classifications'],
        'indications': request.data['indications'], 'contra_indications': request.data['contras'],
        'side_effects': request.data['sideEffects']
         }
        if Drug.objects.filter(name = request.data['name'].strip()):
            raise serializers.ValidationError('Drug name already exists')
        serializer = DrugSerializer(data=new_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response( e)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'status' : 'Bad request',
            'message': 'Drug could not be created with received data.',
            'errors' : serializer.errors # for example
            }, status=status.HTTP_400_BAD_REQUEST)




class DrugDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.name =  request.data['name']
        instance.brand =  request.data['temp_brands']
        instance.form = DrugForm.objects.get(pk =  request.data['temp_form']) if 'temp_form' in request.data else None
        instance.classifications =  request.data['temp_classifications']
        instance.indications =  request.data['temp_indications']
        instance.contra_indications =  request.data['temp_contra_indications']
        instance.dispense_type = DrugDispenseType.objects.get(pk =  request.data['temp_form']) if 'temp_form' in request.data else None
        instance.side_effects =  request.data['temp_side_effects']
        try:
            instance.save()
        except Exception as e:
            return Response( e)
        
        return Response(status=status.HTTP_200_OK)


class AllergyList(generics.ListCreateAPIView):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'allergy' in self.request.query_params:
            search = self.request.query_params['allergy']
            if search:
                return Allergy.objects.filter(name__icontains =  search.strip())
        return Allergy.objects.all()

    def create(self, request, *args, **kwargs):
        new_data = {'name': request.data['name'].strip(), 'possible_reactions': request.data['possibleReactions'],
        'allergen': request.data['allergen'], 'source': request.data['source'],
        'reacts_with': request.data['reactsWith'], 'clinical_presentation': request.data['clinicalPresentation'],
         }
        if Allergy.objects.filter(name = request.data['name'].strip()):
            raise serializers.ValidationError('Allergy name already exists')
        serializer = AllergySerializer(data=new_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response( e)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'status' : 'Bad request',
            'message': 'Allergy could not be created with received data.',
            'errors' : serializer.errors # for example
            }, status=status.HTTP_400_BAD_REQUEST)



class AllergyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Allergy.objects.all()
    serializer_class = AllergyDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.name =  request.data['name']
        instance.possible_reactions =  request.data['possibleReactions']
        instance.allergen =  request.data['allergen']
        instance.source =  request.data['source']
        instance.reacts_with =  request.data['reactsWith']
        instance.clinical_presentation =  request.data['clinicalPresentation']
        try:
            instance.save()
        except Exception as e:
            print( e)
        
        return Response(status=status.HTTP_200_OK)

class DisablityList(generics.ListCreateAPIView):
    queryset = Disablity.objects.all()
    serializer_class = DisablitySerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'disability' in self.request.query_params:
            search = self.request.query_params['disability'].strip()
            if search:
                return Disablity.objects.filter(name__icontains = search)
        return Disablity.objects.all()


class DisabilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Disablity.objects.all()
    serializer_class = DisablitySerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.name =  request.data['name']
        try:
            instance.save()
        except Exception as e:
            print( e)
        
        return Response(status=status.HTTP_200_OK)


class SymptomList(generics.ListCreateAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class DiseaseList(generics.ListCreateAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'disease' in self.request.query_params:
            search = self.request.query_params['disease']
            if search:
                return Disease.objects.filter(name__icontains =  search.strip())
        return Disease.objects.all()




class DiseaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.name =  request.data['name']
        instance.description =  request.data['description']
        try:
            instance.save()
        except Exception as e:
            print( e)
        
        return Response(status=status.HTTP_200_OK)



class ConcentrationList(generics.ListCreateAPIView):
    queryset = AreaOfConcentration.objects.all()
    serializer_class = ConcentrationSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class KitList(generics.ListCreateAPIView):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'kit' in self.request.query_params:
            search = self.request.query_params['kit']
            if search:
                return Kit.objects.filter(name__icontains =  search.strip())
        return Kit.objects.all()

from django.contrib.auth.hashers import make_password

class ResponderList(generics.ListCreateAPIView):
    queryset = Responder.objects.all()
    serializer_class = ResponderDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'responder' in self.request.query_params:
            search = self.request.query_params['responder'].strip()
            if search:
                return Responder.objects.filter(Q(last_name__icontains =  search)|Q(responder_code__icontains= search) |Q(mobile__icontains= search))\
                .select_related('local_govt', 'state' )\
                .prefetch_related('areas_of_concentration', 'kits')

        return Responder.objects.all().select_related('local_govt', 'state' ).prefetch_related( 
                    'areas_of_concentration', 'kits'
                )

    def create(self, request, *args, **kwargs):
        new_data = {'first_name': request.data['first_name'].strip(), 'last_name': request.data['last_name'], 
        'mobile': request.data['mobile'], 'state': request.data['state'], 'local_govt': request.data['lga'],
        'status': 'ACTIVE' , 'areas_of_concentration': request.data['concentrations'], 'kits': request.data['kits'],
        'password': make_password(request.data['password']), 'gender' : request.data['gender'], 
        'middle_name': request.data['middleName'] 
         }
        new_data['serial_num'] = generate_responder_serial()
        try:
            state_code =State.objects.get(pk = request.data['state']).short_name
        except Exception as e:
            return e
        try:
            lga_code = LocalGovernment.objects.get(pk = request.data['lga']).name[:3].upper()
        except Exception as e:
            return e
        if Member.objects.filter(mobile = request.data['mobile']):
            raise serializers.ValidationError('Responder with mobile already exists')
        new_member = Member()
        new_member.mobile = new_data['mobile']
        new_member.password = new_data['password']
        new_member.is_active = True
        new_member.user_type = 'RES'
        new_member.save()
        new_data['member'] = new_member.id
        new_data['responder_code'] = state_code + lga_code +  new_data['serial_num']
        serializer = ResponderSerializer(data=new_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response(e.message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'status' : 'Bad request',
            'message': 'Responder could not be created with received data.',
            'errors' : serializer.errors # for example
            }, status=status.HTTP_400_BAD_REQUEST)



class ResponderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Responder.objects.all()
    serializer_class = ResponderDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        # instance.employee_code = request.data['employee_code']
        if 'mobile' in request.data:
            member = instance.member
            member.mobile = request.data['mobile']
            member.save()
        instance.first_name =  request.data['first_name']
        instance.middle_name = request.data['middle_name']
        instance.last_name =  request.data['last_name']
        instance.mobile = request.data['mobile']
        instance.kits = request.data['res_kits']
        instance.areas_of_concentration = request.data['aocs']
        #instance.gender = Gender.objects.get(pk = request.data['gender'])
        try:
            instance.local_govt = LocalGovernment.objects.get(pk = request.data['lga'])
        except Exception as e:
            pass
        
        #instance.marital_status = MaritalStatus.objects.get(pk = request.data['marital_status'])
        #instance.employment_type = EmploymentType.objects.get(pk = request.data['employment_type'])
        if  request.data['state']:
            instance.state = State.objects.get(pk = request.data['state'])
        
        try:
            instance.save()
        except Exception as e:
            print( e)
        
        return Response(status=status.HTTP_200_OK)





from subprocess import call
class ResponderProfilePicUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)

    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        std_dir = settings.MEDIA_ROOT + 'responders_pics/'
        if not os.path.exists(std_dir):
            os.mkdir(std_dir)
            try:
                call(['chmod', '-R', '777', settings.MEDIA_ROOT])
            except Exception as e:
                pass
        
        new_data = {'profile_pic': request.data['photo']}
        partial = kwargs.pop('partial', False)
        if instance.profile_pic:
            try:
                os.remove(instance.profile_pic.url)
            except Exception as e:
                return Response( e)
            
        try:
            serializer = self.get_serializer(instance, data=new_data, partial=partial)
        except Exception as e:
            print(e)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(instance.image_url, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.conf import settings

DOCS_DIR = settings.MEDIA_ROOT + 'responder_support/'
class ResponderDocUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)

    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        std_dir = DOCS_DIR
        if not os.path.exists(std_dir):
            os.mkdir(std_dir)
            try:
                call(['chmod', '-R', '777', settings.MEDIA_ROOT])
            except Exception as e:
                pass
        if 'uploads[]' in request.FILES:
            for file in request.FILES.getlist('uploads[]'):
                new_responder_doc = ResponderDocument()
                new_responder_doc.document = file
                new_responder_doc.save()
                instance.supporting_docs.add(new_responder_doc)
            return Response(instance.responder_docs, status=status.HTTP_201_CREATED)
        


class ResponderDocList(generics.ListCreateAPIView):
    queryset = ResponderDocument.objects.all()
    serializer_class = ResponderDocumentSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ResponderDocDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResponderDocument.objects.all()
    serializer_class = ResponderDocumentSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ClientList(generics.ListCreateAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'client' in self.request.query_params:
            search = self.request.query_params['client'].strip()
            if search:
                return ClientProfile.objects.filter(last_name__icontains =  search)\
                .select_related('blood_group', 'genotype' , 'gender', 'hmo')\
                .prefetch_related('allergies', 'diseases', 'disabilities')

        return ClientProfile.objects.all().select_related('blood_group', 'genotype' , 'gender', 'hmo' ).prefetch_related( 
                    'allergies', 'diseases', 'disabilities'
                )



class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.first_name =  request.data['first_name']
        instance.last_name = request.data['last_name']
        instance.middle_name = request.data['middle_name'] if 'middle_name' in request.data else ''
        instance.nick_name = request.data['nick_name']
        instance.middle_name = request.data['middle_name'] if 'middle_name' in request.data else ''
        instance.blood_group =  BloodGroup.objects.get(pk = request.data['blood_group'])
        instance.genotype = Genotype.objects.get(pk = request.data['genotype'] ) 
        instance.emergency_name = request.data['emergency_name']
        instance.emergency_number = request.data['emergency_number']
        instance.allergies =  request.data['allergies_list'] if 'allergies_list' in request.data else []
        instance.diseases =  request.data['diseases_list'] if 'diseases_list' in request.data else []
        instance.disabilities = request.data['disabilities_list'] if 'disabilities_list' in request.data else []
        instance.date_of_birth = request.data['date_of_birth']
        instance.nhis_number =request.data['nhis_number'] if 'nhis_number' in request.data else ''
        instance.hmo = HMO.objects.get(pk = request.data['hmo'])
        # instance.genotype = request.data['genotype']
        try:
            instance.save()
        except Exception as e:
            return e
        
        return Response(status=status.HTTP_200_OK)




class TestCenterList(generics.ListCreateAPIView):
    queryset = TestCenter.objects.all()
    serializer_class = TestCenterSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'tc' in self.request.query_params:
            search = self.request.query_params['tc']
            if search:
                return TestCenter.objects.filter(name__icontains =  search.strip())
        return TestCenter.objects.all()


    def create(self, request, *args, **kwargs):
        new_data = {'name': request.data['name'].strip(), 'address': request.data['address'], 
        'description': request.data['description'], 'state': request.data['state'], 'mobile1': request.data['mobile1'],
        'mobile2': request.data['mobile2'], 
         }
        if TestCenter.objects.filter(name = request.data['name'].strip()):
            raise serializers.ValidationError('Drug name already exists')
        serializer = TestCenterSerializer(data=new_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response( e)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'status' : 'Bad request',
            'message': 'Drug could not be created with received data.',
            'errors' : serializer.errors # for example
            }, status=status.HTTP_400_BAD_REQUEST)


class TestCenterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestCenter.objects.all()
    serializer_class = TestCenterDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.name =  request.data['name']
        instance.address = request.data['address']
        instance.mobile1 = request.data['mobile1']
        instance.mobile2 = request.data['mobile2']
        if  request.data['state']:
            instance.state = State.objects.get(pk = request.data['myState'])
        
        try:
            instance.save()
        except Exception as e:
            print (e)
        
        return Response(status=status.HTTP_200_OK)


class PartnersList(generics.ListCreateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'partner' in self.request.query_params:
            search = self.request.query_params['partner']
            if search:
                return Partner.objects.filter(name__icontains =  search.strip())
        return Partner.objects.all()


    def create(self, request, *args, **kwargs):
        new_data = {'name': request.data['name'].strip(), 'address': request.data['address'], 
        'description': request.data['description'], 'state': request.data['state'], 'mobile1': request.data['mobile1'],
        'mobile2': request.data['mobile2'], 
         }
        if Partner.objects.filter(name = request.data['name'].strip()):
            raise serializers.ValidationError('Partner name already exists')
        serializer = PartnerSerializer(data=new_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response( e)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'status' : 'Bad request',
            'message': 'Partner could not be created with received data.',
            'errors' : serializer.errors # for example
            }, status=status.HTTP_400_BAD_REQUEST)



class PartnerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.name =  request.data['name']
        instance.address = request.data['address']
        instance.mobile1 = request.data['mobile1']
        instance.mobile2 = request.data['mobile2']
        if  request.data['state']:
            instance.state = State.objects.get(pk = request.data['myState'])
        
        try:
            instance.save()
        except Exception as e:
            print( e)
        
        return Response(status=status.HTTP_200_OK)


class GenderList(generics.ListCreateAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)



from django.contrib.auth.hashers import make_password


class UserList(generics.ListCreateAPIView):
    # queryset = Member.objects.all()
    serializer_class = SystemUserSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'user' in self.request.query_params:
            search = self.request.query_params['user'].strip()
            if search:
                return Member.objects.filter(Q(user_type__iexact = 'AD') |Q(user_type__iexact= 'SA')).filter(mobile__iexact = search)

        return Member.objects.filter(Q(user_type__iexact = 'AD') |Q(user_type__iexact= 'SA')) #.filter(user_type__iexact =  'AD')


    def create(self, request, *args, **kwargs):
        new_data = {'mobile': request.data['mobile'].strip(), 'user_type': request.data['userType'], 
        'password': make_password(request.data['password']), 
        'email': request.data['email'] if 'email' in request.data else ''
         }
        if Member.objects.filter(mobile = request.data['mobile'].strip()):
            # raise serializers.ValidationError('User with mobile already exists')
            return Response({ 'message': 'User with mobile already exists.'}
                        , status=status.HTTP_400_BAD_REQUEST)
        if not(request.data['password'] == request.data['confPassword']):
            return Response({ 'message': 'Password fields do not match.'}
                        , status=status.HTTP_400_BAD_REQUEST)('Passwords do not match')
        serializer = SystemUserSerializer(data=new_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response( e)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'status' : 'Bad request',
            'message': 'User could not be created with received data.',
            'errors' : serializer.errors # for example
            }, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = SystemUserSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.mobile =  request.data['mobile']
        instance.user_type = request.data['userType']
        instance.email = request.data['email']
        
        try:
            instance.save()
        except Exception as e:
            print( e)
        
        return Response(status=status.HTTP_200_OK)





class NewsletterList(generics.ListCreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'newsletter' in self.request.query_params:
            search = self.request.query_params['newsletter']
            if search:
                return Newsletter.objects.filter(title__icontains =  search.strip())
        return Newsletter.objects.all()


    def create(self, request, *args, **kwargs):
        new_data = {'title': request.data['title'].strip(), 'message': request.data['msg'],
         }
        if Newsletter.objects.filter(title = request.data['title'].strip()):
            raise serializers.ValidationError('Title already exists')
        serializer = NewsletterSerializer(data=new_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response( e)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'status' : 'Bad request',
            'message': 'Newsletter could not be created with received data.',
            'errors' : serializer.errors # for example
            }, status=status.HTTP_400_BAD_REQUEST)



class NewsletterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.title =  request.data['title']
        instance.message = request.data['message']
        
        try:
            instance.save()
        except Exception as e:
            print( e)
        
        return Response(status=status.HTTP_200_OK)



class NewsletterState(generics.RetrieveUpdateDestroyAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request,  *args, **kwargs):
        instance = self.get_object()
        if request.data['status'] =='Ready':
            instance.ready()
        elif request.data['status'] =='Send':
            instance.send()
        
        return Response(status=status.HTTP_200_OK)




class SubscriberList(generics.ListCreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        if 'email' in self.request.query_params:
            search = self.request.query_params['email']
            if search:
                return Subscriber.objects.filter(email__icontains =  search.strip())
        return Subscriber.objects.all()


    def create(self, request, *args, **kwargs):
        new_data = {'email': request.data['email'].strip(), 
         }
        if Subscriber.objects.filter(email = request.data['email'].strip()):
            raise serializers.ValidationError('Subscriber email already exists')
        serializer = SubscriberSerializer(data=new_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                raise e
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'status' : 'Bad request',
            'message': 'Subscriber could not be created with received data.',
            'errors' : serializer.errors # for example
            }, status=status.HTTP_400_BAD_REQUEST)



class SubscriberDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
