from django.db import models

from django.contrib.auth.models import User

from oauth2client.contrib.django_util.models import CredentialsField
from oauth2client.contrib.django_util.models import FlowField



# Create your models here.
class CredetialsModel(models.Model):
	user_id = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True)
	credential = CredentialsField()

class FlowModel(models.Model):
	flow = FlowField()

class SheetModel(models.Model):
	sheetID = models.CharField(max_length=400)
	name = models.CharField(max_length=120)