import os
import locale
import pathlib
import webbrowser

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from passlib.hash import pbkdf2_sha256 as hasher

from datetime import datetime
from Movies import settings
from webapp.database import *
from webapp.forms import MovieEditForm, CategoryForm, CreateUserForm, PaymentCash
from webapp.models import GeeksModel, ImgMovie


def home_page(request):
    locale.setlocale(locale.LC_TIME, '')
    today = datetime.today()
    day_name = today.strftime('%A')

    return render(request, 'home.html', {'day': day_name})


def movies_page(request):
    if request.method == 'GET':
        movies = get_movies()
        return render(request, 'movies.html', {'movies': movies})

    else:
        movie_keys = request.form.getlist('movie_keys')

        for movie_key in movie_keys:
            image = get_image(movie_key)
            if image:
                route = 'static/images/upload/movies/' + image
                os.remove(route)  # borrar primero la imagen del directorio

            delete_movie(int(movie_key))

        return redirect('movies_page')


def movie_page(request, movie_key):
    movie = get_movie(movie_key)

    if movie is None:
        return render(request, 'page_404.html')

    return render(request, 'movie.html', {'movie': movie})


@login_required
def movie_add_page(request):
    form = MovieEditForm()

    if request.method == 'POST':
        form = MovieEditForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data['titulo']
            year = form.cleaned_data['year']
            category = form.cleaned_data['categoria']
            country = form.cleaned_data['pais']
            image = form.cleaned_data.get('imagen')
            stock = form.cleaned_data['stock']
            price = form.cleaned_data['precio']

            if image:
                obj = ImgMovie.objects.create(title=title, img=image)
                obj.save()
                movie = Movie(title, year, category, country, str(image), stock, price)
            else:
                movie = Movie(title, year, category, country, None, stock, price)

            movie_key = add_movie(movie)
            return redirect('movie_page', movie_key=movie_key)
        else:
            print(form)

    return render(request, 'movie_edit.html', {'form': form})


# @login_required
def movie_edit_page(request, movie_key):
    movie = get_movie(movie_key)

    if movie is None:
        return render(request, 'page_404.html')

    if request.method == 'POST':
        form = MovieEditForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['titulo']
            year = form.cleaned_data['year']
            category = form.cleaned_data['categoria']
            country = form.cleaned_data['pais']
            image = form.cleaned_data.get('imagen')
            stock = form.cleaned_data['stock']
            price = form.cleaned_data['precio']

            if image:
                obj = ImgMovie.objects.create(title=title, img=image)
                obj.save()
                movie = Movie(title, year, category, country, str(image), stock, price)
            else:
                movie = Movie(title, year, category, country, None, stock, price)

            update_movie(movie_key, movie)
            return redirect('movie_page', movie_key=movie_key)

    form = MovieEditForm()
    form.fields['titulo'].initial = movie.title
    form.fields['year'].initial = movie.year
    form.fields['categoria'].initial = get_id('Category', 'id_category', movie.category)
    form.fields['pais'].initial = get_id('Country', 'id_country', movie.country)
    form.fields['stock'].initial = movie.stock
    form.fields['precio'].initial = movie.price

    return render(request, 'movie_edit.html', {'form': form})


# @login_required
def categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        category = form.data['categoria']
        cat = add_category(category)

        if cat:
            return redirect('categories')

    cat = get_categories()
    form = CategoryForm()

    return render(request, 'category_edit.html', {'form': form, 'cat': cat})


# @login_required
def delete_category(request, id_category):
    delete_category_db(id_category)

    return redirect('categories')


# @login_required
def profile(request):
    data = get_user(str(request.user))
    return render(request, 'profile.html', {'data': data})


# @login_required
def manage_users(request):
    return render(request, 'manage_users.html')


def create_user(request):
    form = CreateUserForm()

    if request.method == 'POST':
        username = form.data['username'].strip()  # Quitar espacios restantes
        password = form.data['password']
        hashed = hasher.hash(password)  # Contraseña enmascarada

        name = form.data['name'].strip()  # Quitar espacios restantes
        last_name = form.data['lastname'].strip()  # Quitar espacios restantes
        address = form.data['address'].strip()  # Quitar espacios restantes
        telephone = form.data['phone'].strip()
        date_birth = form.data['dateBirth']
        role = form.data['role']
        image = form.data['image']

        if image:
            image_name = username
            date = datetime.now().strftime('%Y%m%d')
            time = datetime.now().strftime('%H%M%S')
            extension = pathlib.Path(image.filename).suffix
            filename = image_name + date + time + extension

            image.save(os.path.join(settings.UPLOAD_FOLDER_PROFILE, filename))
            user = (None, name, last_name, address, telephone if telephone else None,
                    date_birth if date_birth else None, role, filename, username, None)

        else:
            user = (None, name, last_name, address, telephone if telephone else None,
                    date_birth if date_birth else None, role, None, username, None)

        user_exists = get_user(username)

        if user_exists:
            print('Nombre de usuario no disponible')
        else:
            create_user_db(user)
            return redirect('manage_users')

    return render(request, 'user_edit.html', {'form': form})


# @login_required
def users_edit(request):
    users = get_users()
    return render(request, 'users.html', {'users': users, 'action': 'edit'})


# @login_required
def delete_users(request):
    users = get_users()
    return render(request, 'users.html', {'users': users, 'action': 'delete'})


# @login_required
def delete_user(id_user):
    delete_user_db(id_user)
    return redirect('manage_users')


def registro(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)

        if form.is_valid():
            if request.POST['password1'] == request.POST['password2']:
                try:
                    username = request.POST['username']
                    password = request.POST['password1']
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    login(request, user)

                    name = form.data['nombre']
                    lastname = form.data['apellidos']
                    telephone = form.data['telefono']
                    age = form.data['edad']
                    role = 'Normal user'
                    image = form.cleaned_data.get('imagen')

                    if image:
                        obj = GeeksModel.objects.create(title=username, img=image)
                        obj.save()
                        u = User_Class(0, name, lastname, telephone, age, role, str(image), username, password)
                    else:
                        u = User_Class(0, name, lastname, telephone, age, role, None, username, password)

                    create_user_db(u)
                    return redirect('inicio')
                except:
                    return HttpResponse('Ya existe un usuario con ese nombre')
            else:
                return render(request, 'registro.html', {
                    'form_login': UserCreationForm,
                    'form_create': CreateUserForm,
                    'error': 'Las contraseñas no coinciden'
                })
        else:
            print(form)

    return render(request, 'registro.html', {'form_login': UserCreationForm, 'form_create': CreateUserForm})


def login_page(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña invalidos'
            })
        else:
            login(request, user)
            return redirect('inicio')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('inicio')


# @login_required
def edit_profile(request, username):
    user_data = get_user(username)

    if not user_data:
        return render(request, 'page_404.html')

    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['usuario']  # Quitar espacios restantes
            hashed = hasher.hash(form.cleaned_data['password'])  # Contraseña enmascarada
            user_exists = get_user(username)

            if user_exists:
                print('Nombre de usuario no disponible')

            name = form.data['nombre']  # Quitar espacios restantes
            lastname = form.data['apellidos']  # Quitar espacios restantes
            address = form.data['direccion']  # Quitar espacios restantes
            telephone = form.data['telefono']
            date_birth = form.data['fec_nac']
            role = 'Normal user'
            image = form.cleaned_data.get('imagen')

            if image:
                obj = GeeksModel.objects.create(title=username, img=image)
                obj.save()
                user = User_Class(0, name, lastname, address, telephone, date_birth, role, str(image), username, hashed)
            else:
                user = User_Class(0, name, lastname, address, telephone, date_birth, role, None, username, hashed)

            update_user(user)

        return redirect('profile')

    form = CreateUserForm()
    form.fields['usuario'].initial = user_data.username
    form.fields['nombre'].initial = user_data.name
    form.fields['apellidos'].initial = user_data.last_name
    form.fields['direccion'].initial = user_data.address
    form.fields['telefono'].initial = user_data.phone
    form.fields['fec_nac'].initial = user_data.date_birth
    form.fields['role'].initial = user_data.role

    return render(request, 'user_edit.html', {'form': form, 'action': 'edit'})


# @login_required
def add_to_cart(request, movie_key):
    movie = get_movie(movie_key)

    if not movie or movie.stock == 0:
        return render(request, 'page_404.html')

    if request.method == 'POST':
        id_user = 1
        id_movie = movie_key
        add_movie_to_cart(id_user, id_movie)

        return redirect('movies_page')

    return render(request, 'add_to_cart.html', {'movie': movie})


# @login_required
def my_cart(request):
    if request.method == 'POST':
        delete_all_my_movies(1)
        return redirect('my_cart')

    movies = get_my_cart(1)
    total = 0
    for movie in movies:
        total += movie.get('price')

    return render(request, 'my_cart.html', {'movies': movies, 'total': total})


# @login_required
def delete_my_movie(my_movie_key):
    delete_my_movie_db(my_movie_key)
    return redirect('my_cart')


# @login_required
def payment(request):
    movies = get_my_cart(1)

    if not movies:
        return render(request, 'page_401.html')

    return render(request, 'payment.html')


# @login_required
def payment_cash(request):
    form = PaymentCash()

    movies = get_my_cart(1)

    if not movies:
        return render(request, 'page_401.html')

    total = 0
    for movie in movies:
        total += movie.get('price')

    if request.method == 'POST':
        cantidad_recibida = form.data['cantidad']

        if cantidad_recibida >= total:
            id_sale = payment_cash(1, total)
            webbrowser.open_new_tab(request.url_root + 'ticket/' + str(id_sale))

            context = {
                'form': form,
                'total': cantidad_recibida - total,
                'success': True
            }

            return render(request, 'payment_cash.html', context)
        else:
            print('Error de pago, la cantidad no es suficiente')

    return render(request, 'payment_cash.html', {'form': form, 'total': total, 'success': False})


# @login_required
def ticket(request, id_sale):
    date_sale, items, total = get_ticket_items(id_sale, 1)

    if items:
        return render(request, 'ticket.html', {'date': date_sale, 'items': items, 'total': total})
    else:
        return render(request, 'page_404.html')


# @login_required
def my_shopping(request):
    id_shopping = get_my_shopping(1)
    detail_shopping = get_detail_shopping(1)

    empty = True if id_shopping else False

    return render(request, 'my_shopping.html', {'id': id_shopping, 'detail': detail_shopping, 'empty': empty})


# @login_required
def report_sales(request):
    reports = report_sales()
    return render(request, 'report_sales.html', {'reports': reports})


def about(request):
    return render(request, 'about.html')
