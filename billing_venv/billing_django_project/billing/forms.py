from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from product_grocery.models import Product
from .models import Feedback, CartItem


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


class CartItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
