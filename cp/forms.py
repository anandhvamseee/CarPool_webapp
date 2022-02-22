
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
    ('LGBTQ', 'LGBTQ'),
)

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username','email','password1','password2']


class UserProfileForm(forms.ModelForm):
	gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
	class Meta:
		model = UserProfile
		fields = ['gender']

