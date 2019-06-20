from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Action(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="actions")
   verb = models.CharField(max_length=255)
   created = models.DateTimeField(auto_now_add=True)

   targetContentType = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Target ContentType")
   targetID = models.PositiveIntegerField(null=True, blank=True, verbose_name="Target ID")
   target = GenericForeignKey("targetContentType", "targetID")


   def __unicode__(self):
      return "%s %s%s" % (self.user, self.verb, (" " + str(self.target)) if self.target else "")


   class Meta:
      ordering = ("-created",)
