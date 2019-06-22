from __future__ import unicode_literals

from django.db import models
# from django.contrib.auth.models import (
#     BaseUserManager, AbstractBaseUser
# )

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# Create your models here.
class StateManager(models.Manager):
	def get_by_natural_key(self, short_name):
		return self.get(short_name = short_name)

class State(models.Model):
	objects= StateManager()
	name = models.CharField(max_length=50, unique=True)
	short_name = models.CharField(max_length=3, unique=True)


class LocalGovernment(models.Model):
	name = models.CharField(max_length=100)
	state = models.ForeignKey(State)

class AreaOfConcentration(models.Model):
	name = models.CharField(max_length=40, unique=True)

	class Meta:
		ordering = ["name"]


class Equipment(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ["name"]

class Gender(models.Model):
	name = models.CharField(max_length=40, unique=True)

	class Meta:
		ordering = ["name"]


class BloodGroup(models.Model):
	name = models.CharField(max_length=3, unique=True)

	class Meta:
		ordering = ["name"]

class BloodType(models.Model):
	blood_type = models.ForeignKey(BloodGroup)

	


class Genotype(models.Model):
	name = models.CharField(max_length=3, unique =True)

	class Meta:
		ordering = ["name"]


class Allergy(models.Model):
	name = models.CharField(max_length=100, unique=True)
	possible_reactions = models.TextField()
	allergen = models.TextField()
	source = models.TextField()
	reacts_with = models.TextField()
	clinical_presentation = models.TextField()

	class Meta:
		ordering = ["name"]




class SubscriptionType(models.Model):
	name = models.CharField(max_length=100, unique=True)


class DrugClassification(models.Model):
	name = models.CharField(max_length=100, unique =True)

class DrugBrand(models.Model):
	name = models.CharField(max_length=100, unique=True)


class DrugForm(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ["name"]

class DrugDispenseType(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ["name"]


class DrugSideEffect(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ["name"]

class DrugIndication(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ["name"]

class DrugContraIndication(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ["name"]

class Drug(models.Model):
	name = models.CharField(max_length=100)
	brand = models.ManyToManyField(DrugBrand)
	form = models.ForeignKey(DrugForm)
	dispense_type = models.ForeignKey(DrugDispenseType)
	classifications = models.ManyToManyField(DrugClassification)
	indications = models.ManyToManyField(DrugIndication)
	contra_indications = models.ManyToManyField(DrugContraIndication)
	side_effects =  models.ManyToManyField(DrugSideEffect)


	class Meta:
		ordering = ["name"]


class Symptom(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ["name"]

class Disablity(models.Model):
	name = models.CharField(max_length=40, unique=True)

	class Meta:
		ordering = ["name"]


class Disease(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField()
	syptoms = models.ManyToManyField(Symptom, null=True)

	class Meta:
		ordering = ["name"]



class MyUserManager(BaseUserManager):
    def create_user(self, mobile,  password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not mobile:
            raise ValueError('Users must have an mobile')

        user = self.model(
            mobile= mobile,
        
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password):
        """
        Creates and saves a superuser with the given mobile, date of
        birth and password.
        """
        user = self.create_user(
            mobile,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class Member(AbstractBaseUser, PermissionsMixin):
	USER_TYPE_CHOICES = (   
		('SU', 'Super User'), 
		('CL', 'Client'),
        ('RES', 'Responder'), 
        ('AD', 'Admin'),
         ('SA', 'Sub-Admin'),
        )
	mobile = models.CharField(max_length=11, unique=True,)
	is_active = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES)
	email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
	

	objects = MyUserManager()

	USERNAME_FIELD = 'mobile'


	@property
	def user_role_type(self):
	    return self.get_user_type_display()
	


    
class Kit(models.Model):
	name = models.CharField(max_length= 50, unique=True)

class Responder(models.Model):
	RESPONDER_STATUS = (   
		('ACTIVE', 'Active'), 
		('INACTIVE', 'Inactive'),
        )
	member = models.OneToOneField(Member,  on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100, null=True)
	serial_num = models.CharField(max_length=3, unique=True)
	responder_code = models.CharField(max_length=9, unique=True)
	gender = models.ForeignKey(Gender)
	state = models.ForeignKey(State)
	local_govt = models.ForeignKey(LocalGovernment)
	status = models.CharField(max_length=10, choices=RESPONDER_STATUS)
	areas_of_concentration = models.ManyToManyField(AreaOfConcentration, null=True)
	kits = models.ManyToManyField(Kit, null=True)
	profile_pic = models.ImageField(upload_to='responders_pics', null=True)
	supporting_docs = models.ManyToManyField('ResponderDocument', null=True)



	@property
	def image_url(self):
		if self.profile_pic: return self.profile_pic.url

	
	@property
	def responder_docs(self):
		docs = []
		if self.supporting_docs.all():
			for doc in  self.supporting_docs.all(): 
				docs.append({'id' : doc.id , 'doc' :doc.document.url })
			return docs

	class Meta:
		ordering = ["responder_code"]



class DocumentType(models.Model):
	name = models.CharField(max_length=50, unique=True)

	class Meta:
		ordering = ["name"]

class ResponderDocument(models.Model):
	document = models.FileField(upload_to='responder_support', blank=True, null=True)



class HMO(models.Model):
	name = models.CharField(max_length=100, unique=True)
	address = models.CharField(max_length=100)
	state = models.ForeignKey(State)
	mobile1 = models.CharField(max_length=11)
	mobile2  = models.CharField(max_length=11)

	class Meta:
		ordering = ["name"]

class ClientProfile(models.Model):
	CLIENT_STATUS = (   
		('V', 'Verified'), 
		('UV', 'Unverified'),
        )
	client = models.OneToOneField(Member, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100, blank=True, null=True)
	nick_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField()
	gender = models.ForeignKey(Gender)
	genotype = models.ForeignKey(Genotype)
	blood_group = models.ForeignKey(BloodGroup)
	allergies = models.ManyToManyField(Allergy,blank=True, null=True)
	diseases = models.ManyToManyField(Disease, blank=True, null=True)
	disabilities = models.ManyToManyField(Disablity, blank=True, null=True)
	contact_address = models.CharField(max_length=100, unique=True)
	hmo = models.ForeignKey(HMO, null=True)
	nhis_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
	emergency_name = models.CharField(max_length=100)
	emergency_number = models.CharField(max_length=100)
	status = models.CharField(max_length=2, choices=CLIENT_STATUS)

	@property
	def full_name(self):
	    return self.first_name  + ' '  + (self.middle_name + ' ' if self.middle_name else '' )+ self.last_name
	

	@property
	def age(self):
		from datetime import date
		days_in_year = 365.2425
		age = int((date.today() - self.date_of_birth).days / days_in_year)
		return age




class SMSVerification(models.Model):
	user = models.ForeignKey(Member)
	verified = models.BooleanField(default= False)
	#pin =  RandomPinField(length=4)
	sent = models.BooleanField(default=False)
	#phone = PhoneNumberField(null=False, blank=False)


class TestCenter(models.Model):
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField()
	address = models.CharField(max_length=100)
	state = models.ForeignKey(State)
	mobile1 = models.CharField(max_length=11)
	mobile2  = models.CharField(max_length=11)



class Partner(models.Model):
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField()
	address = models.CharField(max_length=100)
	state = models.ForeignKey(State)
	mobile1 = models.CharField(max_length=11)
	mobile2  = models.CharField(max_length=11)




class PasswordReset(models.Model):
	client = models.ForeignKey(Member)
	email = models.EmailField()
	token = models.CharField(max_length=30, unique=True)
	expiry = models.DateField()