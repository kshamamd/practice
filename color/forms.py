from django import forms
from .models import Banner, User, CreatorDesign
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.forms import ModelForm

class RegisterUser(UserCreationForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(),label='Gender')
    is_creator = forms.BooleanField(label='Register as a creator')
    class Meta:
        model = User
        fields = ('phone_number', 'username', 'email', 'first_name', 'last_name', 'is_creator', 'gender') 

class UpdateProfile(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(),label='Gender')
    class Meta:
        model = User
        fields = ('phone_number', 'username', 'email', 'first_name', 'last_name', 'gender') 

class CreatorDesignForm(forms.ModelForm):
    
    class Meta:
        model = CreatorDesign
        fields = ("design_description", "design_name", "design_image")
 