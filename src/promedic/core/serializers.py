from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from newsletters.models import Newsletter, Subscriber

class StateSerializer(serializers.ModelSerializer):
	class Meta:
		model = State
		fields = '__all__'



class LocalGovernmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = LocalGovernment
		fields = '__all__'

class LocalGovernmentDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = LocalGovernment
		fields = '__all__'
		depth = 2



class HMOSerializer(serializers.ModelSerializer):
	class Meta:
		model = HMO
		fields = '__all__'


class HMODetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = HMO
		fields = '__all__'
		depth = 2

class GenotypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Genotype
		fields = '__all__'



class BloodGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = BloodGroup
		fields = '__all__'

		
class BloodTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = BloodType
		fields = '__all__'



class DrugClassificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = DrugClassification
		fields = '__all__'

class DrugBrandSerializer(serializers.ModelSerializer):
	class Meta:
		model = DrugBrand
		fields = '__all__'


class DrugIndicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = DrugIndication
		fields = '__all__'


class DrugSideEffectSerializer(serializers.ModelSerializer):
	class Meta:
		model = DrugSideEffect
		fields = '__all__'


class DrugContraIndicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = DrugContraIndication
		fields = '__all__'


		
class DrugFormSerializer(serializers.ModelSerializer):
	class Meta:
		model = DrugForm
		fields = '__all__'


class DrugDispenseTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = DrugDispenseType
		fields = '__all__'


class DrugSerializer(serializers.ModelSerializer):
	class Meta:
		model = Drug
		fields = '__all__'

class DrugDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Drug
		fields = '__all__'
		depth=2



class AllergySerializer(serializers.ModelSerializer):
	class Meta:
		model = Allergy
		fields = '__all__'


class AllergyDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Allergy
		fields = '__all__'
		depth = 2


class DisablitySerializer(serializers.ModelSerializer):
	class Meta:
		model = Disablity
		fields = '__all__'



class SymptomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Symptom
		fields = '__all__'	


class DocumentTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = DocumentType
		fields = '__all__'	


class DiseaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Disease	
		fields = '__all__'	



class SystemUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    user_role_type = serializers.CharField(required=False)

    class Meta:
        model = Member
        # fields = '__all__'	
        #fields = ('email', 'first_name', 'last_name', 'is_active', 'role')
        read_only_fields = ('last_login',)
        exclude = ('password',)


class ConcentrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = AreaOfConcentration	
		fields = '__all__'	


class KitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Kit	
		fields = '__all__'	

class ResponderSerializer(serializers.ModelSerializer):
	

	class Meta:
		model = Responder	
		fields =  '__all__'	  


class ResponderDetailSerializer(serializers.ModelSerializer):
	image_url = serializers.ReadOnlyField()
	responder_docs = serializers.ReadOnlyField()

	class Meta:
		model = Responder	
		fields =  '__all__'
		depth= 2



class ClientSerializer(serializers.ModelSerializer):
	age = serializers.IntegerField(required=False)
	
	class Meta:
		model = ClientProfile	
		fields =  '__all__'	 
		depth= 2 



class TestCenterSerializer(serializers.ModelSerializer):

	class Meta:
		model = TestCenter	
		fields =   '__all__'


class TestCenterDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = TestCenter	
		fields =   '__all__'
		depth = 2



class PartnerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Partner	
		fields =   '__all__'

class PartnerDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = Partner	
		fields =   '__all__'
		depth = 2



class GenderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Gender
		fields = '__all__'



class ResponderDocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = ResponderDocument
		fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Newsletter
		fields = '__all__'


class SubscriberSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subscriber
		fields = '__all__'