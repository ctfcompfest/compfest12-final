from django.db import models
from django.db.models import Model 
from django import forms
import uuid
# Create your models here. 
  
class NotepadModel(Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	text = models.TextField() 

class BotQueue(Model):
    id_queue = models.CharField(max_length = 100)

class NotepadForm(forms.ModelForm): 
    # specify the name of model to use 
    class Meta: 
        model = NotepadModel 
        fields = "__all__"