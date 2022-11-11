from datetime import datetime
from django import forms


class MovieEditForm(forms.Form):
    title = forms.CharField(label='Title')
    year = forms.IntegerField(label='Year')
    category = forms.ChoiceField(label='Category')
    country = forms.ChoiceField(label='Country')
    image = forms.FileField(label='Image')
    stock = forms.IntegerField(label='Stock')
    price = forms.IntegerField(label='Price')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.PasswordInput()


class CreateUserForm(forms.Form):
    name = forms.CharField(label='Name')
    lastname = forms.CharField(label='Last Name')
    username = forms.CharField(label='Username')
    password = forms.PasswordInput()
    address = forms.CharField(label='Address')
    phone = forms.CharField(label='Phone')
    dateBirth = forms.DateTimeField(label='Date')
    role = forms.ChoiceField(label='Role', choices=['Admin', 'Normal user'])
    image = forms.FileField()


class CategoryForm(forms.Form):
    category = forms.CharField(label='Category')


class CountryForm(forms.Form):
    country = forms.CharField(label='Country')


class PaymentCash(forms.Form):
    cantidad = forms.IntegerField(label='Cantidad')
