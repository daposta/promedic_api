from rest_framework import serializers
from core.models import *
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        read_only_fields = ('last_login',)
        exclude = ('password',)
   

class GenotypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Genotype
		fields = '__all__'


class GenderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Gender
		fields = '__all__'


class BloodGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = BloodGroup
		fields = '__all__'


class HMOSerializer(serializers.ModelSerializer):
	class Meta:
		model = HMO
		fields = '__all__'


class AllergySerializer(serializers.ModelSerializer):
	class Meta:
		model = Allergy
		fields = '__all__'


class DisablitySerializer(serializers.ModelSerializer):
	class Meta:
		model = Disablity
		fields = '__all__'



class DiseaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Disease	
		fields = '__all__'	


class ClientProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClientProfile	
		fields = '__all__'	


class ExClientProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClientProfile	
		fields = '__all__'
		depth = 2