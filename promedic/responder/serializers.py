from rest_framework import serializers
from core.models import *
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class ResponderSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Responder	
		fields =  '__all__'	  


class ResponderDetailSerializer(serializers.ModelSerializer):
	image_url = serializers.ReadOnlyField()

	class Meta:
		model = Responder	
		fields =   '__all__'
		depth= 2
