from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
# Create your views here.


from core import models
from . import serializers


class StateViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer

class LocalGovernmentViewSet(viewsets.ModelViewSet):
    queryset = models.LocalGovernment.objects.all()
    serializer_class = serializers.LocalGovtSerializer
    #authentication_classes = (JSONWebTokenAuthentication,)
    #permission_classes = (IsAuthenticated,)


class AreaOfConcentrationViewSet(viewsets.ModelViewSet):
    queryset = models.AreaOfConcentration.objects.all()
    serializer_class = serializers.AreaOfConcentrationSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = models.Equipment.objects.all()
    serializer_class = serializers.EquipmentSerializer

class GenderViewSet(viewsets.ModelViewSet):
    queryset = models.Gender.objects.all()
    serializer_class = serializers.GenderSerializer

class BloodGroupViewSet(viewsets.ModelViewSet):
    queryset = models.BloodGroup.objects.all()
    serializer_class = serializers.BloodGroupSerializer

class BloodTypeViewSet(viewsets.ModelViewSet):
    queryset = models.BloodType.objects.all()
    serializer_class = serializers.BloodTypeSerializer

class AllergyViewSet(viewsets.ModelViewSet):
    queryset = models.Allergy.objects.all()
    serializer_class = serializers.AllergySerializers

class SubscriptionTypeViewSet(viewsets.ModelViewSet):
    queryset = models.SubscriptionType.objects.all()
    serializer_class = serializers.SubscriptionTypeSerializers

class DrugClassificationViewSet(viewsets.ModelViewSet):
    queryset = models.DrugClassification.objects.all()
    serializer_class = serializers.DrugClassificationSerializers

class DrugBrandViewSet(viewsets.ModelViewSet):
    queryset = models.DrugClassification.objects.all()
    serializer_class = serializers.DrugClassificationSerializers

class DrugFormViewSets(viewsets.ModelViewSet):
    queryset = models.DrugForm.objects.all()
    serializer_class = serializers.DrugFormSerializers

class DrugDispenseTypeViewSet(viewsets.ModelViewSet):
    queryset = models.DrugDispenseType.objects.all()
    serializer_class = serializers.DrugDispenseTypeSerializers

class DrugSideEffectViewSet(viewsets.ModelViewSet):
    queryset = models.DrugSideEffect.objects.all()
    serializer_class = serializers.DrugSideEffectSerializers

class DrugIndicationViewSets(viewsets.ModelViewSet):
    queryset = models.DrugContraIndication.objects.all()
    serializer_class = serializers.DrugIndicationSerializers

class DrugContraIndicationViewSet(viewsets.ModelViewSet):
    queryset = models.DrugContraIndication.objects.all()
    serializer_class = serializers.DrugContraIndicationSerializers

class DrugViewSet(viewsets.ModelViewSet):
    queryset = models.Drug.objects.all()
    serializer_class = serializers.DrugSerializers
    
class SymptomViewsets(viewsets.ModelViewSet):
    queryset = models.Symptom.objects.all()
    serializer_class = serializers.SymptomSerializers

class DisablityViewsets(viewsets.ModelViewSet):
    queryset = models.Disablity.objects.all()
    serializer_class = serializers.DisablitySerializers

class DiseaseViewsets(viewsets.ModelViewSet):
    queryset = models.Disease.objects.all()
    serializer_class = serializers.DiseaseSerializers

class UserViewsets(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializers
 
class KitViewsets(viewsets.ModelViewSet):
    queryset = models.Kit.objects.all()
    serializer_class = serializers.KitSerializers

class ResponderViewsets(viewsets.ModelViewSet):
    queryset = models.Responder.objects.all()
    serializer_class = serializers.ResponderSerializers

    


"""
class MemberViewsets(viewsets.ModelViewSet):
    queryset =  models.Member.objects.all()
    serializer_class = serializers.MemberSerializers
"""




















































