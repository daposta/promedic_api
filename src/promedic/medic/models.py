from __future__ import unicode_literals

from django.db import models

# Create your models here.
class MedicRequest(models.Model):
	timestamp = models.DateTimeField(auto_now_add =True)
	querystring = models.CharField(max_length=100)
	sender_number = models.CharField(max_length=15)