import os
import locale
import pathlib
import webbrowser
from datetime import datetime

from Movies import settings
from webapp.database import *
from django.shortcuts import render, redirect
from passlib.hash import pbkdf2_sha256 as hasher
from django.contrib.auth.decorators import login_required
from webapp.forms import MovieEditForm, CategoryForm, CreateUserForm, PaymentCash
from webapp.models import Movie


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


# @login_required
def movie_add_page(request):
    form = MovieEditForm()

    if request.method == 'POST':
        title = form.data['title']
        year = form.data['year']
        category = form.data['category']
        country = form.data['country']
        image = form.data['image']
        stock = form.data['stock']
        price = form.data['price']

        if image:
            image_name = title
            date = datetime.now().strftime('%Y%m%d')
            time = datetime.now().strftime('%H%M%S')
            extension = pathlib.Path(image.filename).suffix
            filename = image_name + date + time + extension

            image.save(os.path.join(settings.UPLOAD_FOLDER, filename))

            movie = Movie(title, year, category, country, filename, stock, price)
        else:
            movie = Movie(title, year, category, country, None, stock, price)

        movie_key = add_movie(movie)

        return redirect('movie_page', movie_key=movie_key)

    return render(request, 'movie_edit.html', {'form': form})


# @login_required
def movie_edit_page(request, movie_key):
    movie = get_movie(movie_key)

    if movie is None:
        return render(request, 'page_404.html')

    form = MovieEditForm()

    if request.method == 'POST':
        title = form.data['title'].strip()  # Quitar espacios restantes
        year = form.data['year']
        category = form.data['category']
        country = form.data['country']
        image = form.data['image']
        stock = form.data['stock']
        price = form.data['price']

        if image:
            image_name = title
            date = datetime.now().strftime('%Y%m%d')
            time = datetime.now().strftime('%H%M%S')
            extension = pathlib.Path(image.filename).suffix
            filename = image_name + date + time + extension
            image.save(os.path.join(settings.UPLOAD_FOLDER, filename))

            movie = Movie(title, year, category, country, filename, stock, price)

            old_image = get_image(movie_key)
            if old_image:
                url = 'static/images/upload/movies/' + old_image
                os.remove(url)  # borrar la imagen anterior

        else:
            movie = Movie(title, year, category, country, None, stock, price)

        update_movie(movie_key, movie)

        return redirect('movie_page', movie_key=movie_key)

    form.fields['title'].initial = movie.title
    form.fields['year'].initial = movie.year
    form.fields['category'].initial = get_id('Category', 'id_category', movie.category)
    form.fields['country'].initial = get_id('Country', 'id_country', movie.country)
    form.fields['stock'].initial = movie.stock
    form.fields['price'].initial = movie.price

    return render(request, 'movie_edit.html', {'form': form})


# @login_required
def categories(request):
    form = CategoryForm()

    if request.method == 'POST':
        category = form.data['category'].strip()
        cat = add_category(category)

        if cat:
            return redirect('categories')

    cat = get_categories()

    return render(request, 'category_edit.html', {'form': form, 'cat': cat})


# @login_required
def delete_category(request, id_category):
    delete_category_db(id_category)

    return redirect('categories')


# @login_required
def profile(request):
    return render(request, 'profile.html')


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


# @login_required
def edit_profile(request, username):
    form = CreateUserForm()
    user_data = get_user(username)

    if not user_data:
        return render(request, 'page_404.html')

    if request.method == 'POST':
        name = form.data['name']
        lastname = form.data['lastname']
        address = form.data['address']
        telephone = form.data['phoneNumber']
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
            user = (None, name, lastname, address, telephone if telephone else None,
                    date_birth if date_birth else None, role, filename, username, None)
        else:
            user = (None, name, lastname, address, telephone if telephone else None,
                    date_birth if telephone else None, role, None, username, None)

        update_user(user)

        return redirect('profile')

    form.username.data = user_data.username
    form.name.data = user_data.name
    form.lastname.data = user_data.lastName
    form.address.data = user_data.address
    form.phone.data = user_data.phone
    form.dateBirth.data = user_data.dateBirth
    form.role.data = user_data.role

    return render(request, 'user_edit.html', {'form': form})


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
