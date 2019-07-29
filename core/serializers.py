from rest_framework import serializers
from . import models

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = ('name', 'short_name',)


class LocalGovtSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LocalGovernment
        fields = ('name', 'state',)

class AreaOfConcentrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AreaOfConcentration
        fields = ('name', )

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Equipment
        fields = ('name',)

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gender
        fields = ('name',)

class BloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BloodGroup
        fields = ('name',)

class BloodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BloodType
        fields = ('blood_type',)

class AllergySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Allergy
        fields = ('name', 'possible_reactions', 'allergen', 'source', 'reacts_with', 'clinical_presentation')

class SubscriptionTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.SubscriptionType
        fields = ('name',)

class DrugClassificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DrugClassification
        fields = ('name',)

class DrugBrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DrugBrand
        fields = ('name',)
  
class DrugFormSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DrugForm
        fields = ('name',)

class DrugDispenseTypeSerializers():
    class Meta:
        model = models.DrugDispenseType
        fields = ('name',)

class DrugSideEffectSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DrugSideEffect
        fields = ('name') 

class DrugIndicationSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DrugIndication
        fields = ('name')

class DrugContraIndicationSerializers():
    class Meta:
        model =  models.DrugContraIndication
        fields = ('name')

class DrugSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Drug
        fields = ('name', 'brand', 'form', 'dispense_type', 'classifications', 'indications', 'contra_indications', 'side_effects')


class SymptomSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Symptom
        fields = ('name',)

class DisablitySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Disablity
        fields = ('name')

class DiseaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Disease
        fields = ('name', 'description', 'syptoms')

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('phonenumber', 'password')

class KitSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Kit
        fields = ('name',)
 
class ResponderSerializers(serializers.ModelSerializer):
     class Meta:
         model = models.Responder
         fields = ('member', 'first_name', 'last_name', 'middle_name', 
         'serial_num', 'responder_code', 'gender', 'state', 'local_govt', 
         'status', 'areas_of_concentration', 'kits', 'profile_pic', 'supporting_docs',)


"""
class MemberSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ('mobile', 'is_active', 'is_admin', 'user_type', 'email')

        """