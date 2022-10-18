import os
import pathlib
import webbrowser

import database
from movie import Movie
from datetime import datetime
from forms import MovieEditForm, LoginForm, CreateUserForm, CategoryForm, PaymentCash
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import login_required, current_user, login_user, logout_user
from flask import render_template, current_app, abort, request, url_for, redirect, flash
from user import User


def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.data['username']
        user = database.get_user(username)

        if user is not None:
            password = form.data['password']

            if hasher.verify(password, user.password):
                login_user(user)
                flash('You have a logged in.')
                next_page = request.args.get('next', url_for('home_page'))
                return redirect(next_page)

        flash('Invalid credentials.')

    if current_user.is_authenticated:
        flash('You have a logged in.')
        return redirect(url_for('home_page'))

    return render_template('login.html', form=form)


def logout_page():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('home_page'))


def create_user():
    if not current_user.is_admin:
        return render_template('page_401.html')

    if not current_user.username == 'admin':
        return render_template('page_401.html')

    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.data['username'].strip()  # Quitar espacios restantes
        password = form.data['password']
        hashed = hasher.hash(password)  # Contraseña enmascarada

        name = form.data['name'].strip()  # Quitar espacios restantes
        lastname = form.data['lastname'].strip()  # Quitar espacios restantes
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

            image.save(os.path.join(current_app.config['UPLOAD_FOLDER_PROFILE'], filename))
            user = User(None, name, lastname, address, telephone if telephone else None, date_birth if date_birth else None, role, filename, username, hashed)
        else:
            user = User(None, name, lastname, address, telephone if telephone else None, date_birth if telephone else None, role, None, username, hashed)

        user_exists = database.get_user(username)

        if user_exists:
            flash('Username no disponible')
        else:
            database.create_user(user)
            return redirect(url_for('manage_users'))

    return render_template('user_edit.html', form=form)


@login_required
def manage_users():
    if not current_user.is_admin:
        return render_template('page_401.html')

    if not current_user.username == 'admin':
        return render_template('page_401.html')

    return render_template('manage_users.html')


@login_required
def profile():
    return render_template('profile.html')


@login_required
def users_edit():
    if not current_user.is_admin:
        return render_template('page_401.html')

    if not current_user.username == 'admin':
        return render_template('page_401.html')

    users = database.get_users()
    return render_template('users.html', users=users, action="edit")


@login_required
def delete_users():
    if not current_user.is_admin:
        return render_template('page_401.html')

    if not current_user.username == 'admin':
        return render_template('page_401.html')

    users = database.get_users()
    return render_template('users.html', users=users, action="delete")


@login_required
def delete_user(id_user):
    if not current_user.is_admin:
        return render_template('page_401.html')

    database.delete_user(id_user)
    return redirect(url_for('manage_users'))


@login_required
def edit_profile(username):
    if not current_user.is_admin:
        return render_template('page_401.html')

    if not current_user.username == 'admin':
        return render_template('page_401.html')

    form = CreateUserForm()
    user_data = database.get_user(username)

    if not user_data:
        return render_template('page_404.html')

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

            image.save(os.path.join(current_app.config['UPLOAD_FOLDER_PROFILE'], filename))
            user = User(None, name, lastname, address, telephone if telephone else None,
                        date_birth if date_birth else None, role, filename, username, None)
        else:
            user = User(None, name, lastname, address, telephone if telephone else None,
                        date_birth if telephone else None, role, None, username, None)

        database.update_user(user)

        next_page = request.args.get('next', url_for('profile'))
        return redirect(next_page)

    form.username.data = user_data.username
    form.name.data = user_data.name
    form.lastname.data = user_data.lastName
    form.address.data = user_data.address
    form.phone.data = user_data.phone
    form.dateBirth.data = user_data.dateBirth
    form.role.data = user_data.role

    return render_template('user_edit.html', form=form)


def home_page():
    today = datetime.today()
    day_name = today.strftime('%A')
    return render_template('home.html', day=day_name)


def movies_page():
    if request.method == 'GET':
        movies = database.get_movies()
        my_movies_keys = []

        if current_user.is_authenticated:
            my_movies = database.get_my_cart(current_user.id_user)

            for movie in my_movies:
                my_movies_keys.append(movie['id_movie'])

        return render_template('movies.html', movies=movies, my_movies_keys=my_movies_keys)
    else:
        if not current_user.is_admin:
            return render_template('page_401.html')

        movie_keys = request.form.getlist('movie_keys')

        for movie_key in movie_keys:
            image = database.get_image(movie_key)
            if image:
                os.remove('static/images/upload/movies/' + image)  # borrar primero la imagen del directorio

            database.delete_movie(int(movie_key))

        return redirect(url_for('movies_page'))


def movie_page(movie_key):
    movie = database.get_movie(movie_key)

    if movie is None:
        return render_template('page_404.html')

    return render_template('movie.html', movie=movie)


@login_required
def add_to_cart(movie_key):
    movie = database.get_movie(movie_key)

    if not movie:
        return render_template('page_404.html')

    if movie.stock == 0:
        return render_template('page_401.html')

    if request.method == 'POST':
        id_user = current_user.id_user
        id_movie = movie_key
        database.add_movie_to_cart(id_user, id_movie)

        return redirect(url_for('movies_page'))

    return render_template('add_to_cart.html', movie=movie)


@login_required
def my_cart():
    if request.method == 'POST':
        database.delete_all_my_movies(current_user.id_user)
        return redirect(url_for('my_cart'))

    movies = database.get_my_cart(current_user.id_user)
    total = 0
    for movie in movies:
        total += movie.get('price')

    return render_template('my_cart.html', movies=movies, total=total)


@login_required
def delete_my_movie(my_movie_key):
    database.delete_my_movie(my_movie_key)
    return redirect(url_for('my_cart'))


@login_required
def payment():
    movies = database.get_my_cart(current_user.id_user)

    if not movies:
        return render_template('page_401.html')

    return render_template('payment.html')


@login_required
def payment_cash():
    form = PaymentCash()

    movies = database.get_my_cart(current_user.id_user)

    if not movies:
        return render_template('page_401.html')

    total = 0
    for movie in movies:
        total += movie.get('price')

    if form.validate_on_submit():
        cantidad_recibida = form.data['cantidad']

        if cantidad_recibida >= total:
            id_sale = database.payment_cash(current_user.id_user, total)
            webbrowser.open_new_tab(request.url_root + 'ticket/' + str(id_sale))
            return render_template('payment_cash.html', form=form, total=cantidad_recibida-total, success=True)
        else:
            flash('Error de pago, la cantidad no es suficiente')

    return render_template('payment_cash.html', form=form, total=total, success=False)


@login_required
def ticket(id_sale):
    date_sale, items, total = database.get_ticket_items(id_sale, current_user.id_user)

    if items:
        return render_template('ticket.html', date=date_sale, items=items, total=total)
    else:
        return render_template('page_404.html')


@login_required
def my_shopping():
    id_shopping = database.get_my_shopping(current_user.id_user)
    detail_shopping = database.get_detail_shopping(current_user.id_user)

    empty = False
    if not id_shopping:
        empty = True

    return render_template('my_shopping.html', id=id_shopping, detail=detail_shopping, empty=empty)


@login_required
def report_sales():
    reports = database.report_sales()
    return render_template('report_sales.html', reports=reports)


@login_required
def movie_add_page():
    if not current_user.is_admin:
        return render_template('page_401.html')

    form = MovieEditForm()

    form.category.choices.clear()
    form.category.choices = database.get_categories()

    if form.validate_on_submit():
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

            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            movie = Movie(title, year, category, country, filename, stock, price)
        else:
            movie = Movie(title, year, category, country, None, stock, price)

        movie_key = database.add_movie(movie)

        return redirect(url_for('movie_page', movie_key=movie_key))
    else:
        for error in form.errors:
            flash(error + ' - ' + str(form.errors[error][0]))

    return render_template('movie_edit.html', min_year=1887, max_year=datetime.now().year, form=form)


@login_required
def movie_edit_page(movie_key):
    movie = database.get_movie(movie_key)

    if movie is None:
        return render_template('page_404.html')

    if not current_user.is_admin:
        return render_template('page_401.html')

    form = MovieEditForm()

    if form.validate_on_submit():
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

            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            movie = Movie(title, year, category, country, filename, stock, price)

            old_image = database.get_image(movie_key)
            if old_image:
                os.remove('static/images/upload/movies/' + old_image)  # borrar la imagen anterior
        else:
            movie = Movie(title, year, category, country, None, stock, price)

        database.update_movie(movie_key, movie)

        return redirect(url_for('movie_page', movie_key=movie_key))

    form.category.choices.clear()
    form.category.choices = database.get_categories()

    form.title.data = movie.title
    form.year.data = movie.year if movie.year else ''
    form.category.data = movie.category
    form.country.data = movie.country
    form.stock.data = movie.stock
    form.price.data = movie.price

    return render_template('movie_edit.html', form=form)


@login_required
def categories():
    if not current_user.is_admin:
        return render_template('page_401.html')

    form = CategoryForm()

    if form.validate_on_submit():
        category = form.data['category']
        cat = database.add_category(category)

        if cat:
            flash('Successfully added')
            return redirect(url_for('categories'))
        else:
            flash('Already exists')

    cat = database.get_categories()
    return render_template('category_edit.html', form=form, cat=cat)


@login_required
def delete_category(id_category):
    if not current_user.is_admin:
        return render_template('page_401.html')

    database.delete_category(id_category)
    flash('Removed successfully')

    return redirect(url_for('categories'))


def about():
    return render_template('about.html')


def valdiate_movie_form(form):
    form.data = {}
    form.errors = {}

    title = form.get('title', '').strip()
    if len(title) == 0:
        form.errors['title'] = 'Title can not be blank'
    else:
        form.data['title'] = title

    year = form.get('year')
    if not year:
        form.data['year'] = None
    elif not year.isdigit():
        form.errors['year'] = 'Year must consist of digits only'
    else:
        y = int(year)
        if (y < 1887) or (y > datetime.now().year):
            form.errors['year'] = 'Year not in valid range'
        else:
            form.data['year'] = y

    return len(form.errors) == 0