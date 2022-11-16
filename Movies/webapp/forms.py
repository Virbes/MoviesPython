from django import forms
from webapp.database import get_categories, get_countries


class MovieEditForm(forms.Form):
    category_choices = get_categories()
    country_choices = get_countries()

    titulo = forms.CharField(label='Titulo', required=True,
                             widget=forms.TextInput(attrs={'class': 'input', 'autofocus': 'true'}))
    año = forms.IntegerField(label='Año', required=True,
                             widget=forms.NumberInput(attrs={'class': 'input'}))
    categoria = forms.ChoiceField(label='Categoria', required=True, choices=category_choices,
                                  widget=forms.Select(attrs={'class': 'input'}))
    pais = forms.ChoiceField(label='Pais', required=True, choices=country_choices,
                             widget=forms.Select(attrs={'class': 'input'}))
    stock = forms.IntegerField(label='Stock', required=True,
                               widget=forms.TextInput(attrs={'class': 'input'}))
    precio = forms.IntegerField(label='Precio', required=True,
                                widget=forms.NumberInput(attrs={'class': 'input'}))
    imagen = forms.ImageField(label='Imagen')


class LoginForm(forms.Form):
    usuario = forms.CharField(label='Usuario')
    contraseña = forms.PasswordInput()


class CreateUserForm(forms.Form):
    nombre = forms.CharField(label='Nombre', required=True,
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'input is-large',
                                     'placeholder': 'Nombre',
                                     'autofocus': 'true'
                                 }
                             ))
    apellidos = forms.CharField(label='Apellidos', required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'input is-large',
                                        'placeholder': 'Apellidos'
                                    }
                                ))
    usuario = forms.CharField(label='Usuario', required=True,
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'input is-large',
                                      'placeholder': 'Usuario'
                                  }
                              ))
    password = forms.CharField(label='Contraseña', required=True,
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'input is-large',
                                       'placeholder': 'Contraseña'
                                   }
                               ))
    direccion = forms.CharField(label='Direccion', required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'input is-large',
                                        'placeholder': 'Direccion'
                                    }
                                ))
    telefono = forms.CharField(label='Telefono', required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'input is-large',
                                       'placeholder': 'Telefono'
                                   }
                               ))
    fec_nac = forms.CharField(label='Fecha de Nacimiento',
                              widget=forms.TextInput(
                                  attrs={
                                      'type': 'date',
                                      'class': 'form-date__input'}
                              ))
    role = forms.ChoiceField(label='Role', choices=[(1, 'Admin'), (2, 'Normal user')], required=False)
    imagen = forms.ImageField(label='Imagen', required=True)


class CategoryForm(forms.Form):
    categoria = forms.CharField(label='Categoria', required=True,
                                widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Añadir Categoria'}))


class CountryForm(forms.Form):
    country = forms.CharField(label='Country')


class PaymentCash(forms.Form):
    cantidad = forms.IntegerField(label='Cantidad')
