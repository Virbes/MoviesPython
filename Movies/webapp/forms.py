from datetime import datetime
from django import forms

from webapp.database import get_categories, get_countries


class MovieEditForm(forms.Form):
    category_choices = get_categories()
    country_choices = get_countries()

    title = forms.CharField(label='Title', required=True,
                            widget=forms.TextInput(attrs={'class': 'input', 'autofocus': 'true'}))
    year = forms.IntegerField(label='Year', required=True,
                              widget=forms.TextInput(attrs={'class': 'input'}))
    category = forms.ChoiceField(label='Category', required=True, choices=category_choices,
                                 widget=forms.Select(attrs={'class': 'input'}))
    country = forms.ChoiceField(label='Country', required=True, choices=country_choices,
                                widget=forms.Select(attrs={'class': 'input'}))
    stock = forms.IntegerField(label='Stock', required=True,
                               widget=forms.TextInput(attrs={'class': 'input'}))
    price = forms.IntegerField(label='Price', required=True,
                               widget=forms.TextInput(attrs={'class': 'input'}))
    image = forms.ImageField(label='Image', required=True)


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
    category = forms.CharField(label='Category', required=True,
                               widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Añadir Categoria'}))


class CountryForm(forms.Form):
    country = forms.CharField(label='Country')


class PaymentCash(forms.Form):
    cantidad = forms.IntegerField(label='Cantidad')
