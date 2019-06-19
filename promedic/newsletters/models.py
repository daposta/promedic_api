from __future__ import unicode_literals

from django.db import models
from django_fsm import FSMField, transition


# Create your models here.
class Subscriber(models.Model):
	email = models.EmailField(unique=True)
	date_added = models.DateTimeField(auto_now_add=True)
	unsubscribed = models.BooleanField(default=False)


class Newsletter(models.Model):
	title = models.CharField(max_length=100)
	message = models.TextField()
	date_created = models.DateTimeField(auto_now_add= True)
	last_modified = models.DateTimeField(auto_now=True)
	state = FSMField(default='Draft')

	@transition(field=state, source='Draft', target='Ready')
	def ready(self):
		self.state = 'Ready'
		self.save()


	@transition(field=state, source='Ready', target='Send')
	def send(self):
		self.state = 'Sent'
		self.save()
		from .utils import send_newsletter_mail
		subscribers = Subscriber.objects.filter(unsubscribed = False).values_list('email', flat=True)
		send_newsletter_mail(subscribers, self)

