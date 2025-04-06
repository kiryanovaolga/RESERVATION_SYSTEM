from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from reservation.models import User, Service

class UserForm(ModelForm):

    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(), 
        widget=forms.SelectMultiple, 

    )
        


    class Meta:
        model = User
        fields = ['first_name', 'services', 'phone']
    