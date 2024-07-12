from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Feedback
# from billing.models import CustomUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        # model = CustomUser
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        # model = CustomUser
        model = User
        fields = ('username', 'email')

class UserFeedback(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']