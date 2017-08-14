from django import forms
from .models import ndDetail

class NodeDeviceSetForm(forms.ModelForm):
  class Meta:
    model = ndDetail
    fields = ['req_value']
  
  