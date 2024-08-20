from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class BrandCampaignForm(forms.ModelForm):
    class Meta:
        model = BrandCampaign
        fields = ['brand', 'title', 'text']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }