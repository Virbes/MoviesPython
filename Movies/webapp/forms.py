from django import forms
from webapp.database import get_categories, get_countries


class MovieEditForm(forms.Form):
    category_choices = get_categories()
    country_choices = get_countries()

    titulo = forms.CharField(label='Titulo', required=True,
                             widget=forms.TextInput(attrs={'class': 'input', 'autofocus': 'true'}))
    year = forms.IntegerField(label='Año', required=True,
                              widget=forms.NumberInput(attrs={'class': 'input'}))
    categoria = forms.ChoiceField(label='Categoria', required=True, choices=category_choices,
                                  widget=forms.Select(attrs={'class': 'input'}))
    pais = forms.ChoiceField(label='Pais', required=True, choices=country_choices,
                             widget=forms.Select(attrs={'class': 'input'}))
    stock = forms.IntegerField(label='Stock', required=True,
                               widget=forms.TextInput(attrs={'class': 'input'}))
    precio = forms.IntegerField(label='Precio', required=True,
                                widget=forms.NumberInput(attrs={'class': 'input'}))
    imagen = forms.ImageField(label='Imagen', required=False)


class CreateUserForm(forms.Form):
    nombre = forms.CharField(label='Nombre', required=True, widget=forms.TextInput(attrs={
                                     'class': 'input is-medium',
                                     'placeholder': 'Nombre'
                                 }))
    apellidos = forms.CharField(label='Apellidos', required=True, widget=forms.TextInput(attrs={
                                        'class': 'input is-medium',
                                        'placeholder': 'Apellidos'
                                    }))
    telefono = forms.CharField(label='Telefono', required=True, widget=forms.TextInput(attrs={
                                       'class': 'input is-medium',
                                       'placeholder': 'Telefono'
                                   }))
    edad = forms.CharField(label='Fecha de Nacimiento', widget=forms.NumberInput(attrs={
                                      'type': 'number',
                                      'class': 'input is-medium',
                                      'placeholder': 'Edad'
                                  }))
    role = forms.ChoiceField(label='Role', choices=[(1, 'Admin'), (2, 'Normal user')], required=False)
    imagen = forms.ImageField(label='Imagen', required=False)


class CategoryForm(forms.Form):
    categoria = forms.CharField(label='Categoria', required=True,
                                widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Añadir Categoria'}))


class CountryForm(forms.Form):
    country = forms.CharField(label='Country')


class PaymentCash(forms.Form):
    cantidad = forms.IntegerField(label='Cantidad')
