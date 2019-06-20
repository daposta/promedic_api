from rest_framework import serializers
from .models import *

class MedicRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = MedicRequest
		fields = '__all__'