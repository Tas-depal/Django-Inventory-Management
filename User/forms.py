from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model= User
		#the fields to be displayed in the form
		fields = ['username', 'email','password1','password2']

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model=User
		#the fields to be displayed in the form
		fields =['username','email']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model=Profile
		#the fields to be displayed in the form
		fields=['address','phone','image']