import os
import locale
import pathlib
import database
import webbrowser

from user import User
from movie import Movie
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import login_required, current_user, login_user, logout_user
from forms import MovieEditForm, LoginForm, CreateUserForm, CategoryForm, PaymentCash
from flask import render_template, current_app, request, url_for, redirect, flash


def home_page():
    locale.setlocale(locale.LC_TIME, '')
    today = datetime.today()
    day_name = today.strftime('%A')

    db = current_app.config['db']
    movie = db.get_movie(7)

    return render_template('home.html', day=day_name, movie=movie)


def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.data['username']

        db = current_app.config['db']
        user = db.get_user(username)

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


def movies_page():
    db = current_app.config['db']

    if request.method == 'GET':
        movies = db.get_movies()
        return render_template('movies.html', movies=movies)

    else:
        if not current_user.role == 'Admin':
            return render_template('page_401.html')

        movie_keys = request.form.getlist('movie_keys')

        for movie_key in movie_keys:
            image = db.get_image(movie_key)
            if image:
                route = 'static/images/upload/movies/' + image
                os.remove(route)  # borrar primero la imagen del directorio

            db.delete_movie(int(movie_key))

        return redirect(url_for('movies_page'))


def movie_page(movie_key):
    db = current_app.config['db']
    movie = db.get_movie(movie_key)

    if movie is None:
        return render_template('page_404.html')

    return render_template('movie.html', movie=movie)


@login_required
def movie_add_page():
    db = current_app.config['db']

    if not current_user.role == 'Admin':
        return render_template('page_401.html')

    form = MovieEditForm()
    form.category.choices, form.country.choices = get_choices(form)

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

        movie_key = db.add_movie(movie)

        return redirect(url_for('movie_page', movie_key=movie_key))
    else:
        for error in form.errors:
            flash(error + ' - ' + str(form.errors[error][0]))

    return render_template('movie_edit.html', min_year=1887, max_year=datetime.now().year, form=form)


@login_required
def movie_edit_page(movie_key):
    db = current_app.config['db']
    movie = db.get_movie(movie_key)

    if movie is None:
        return render_template('page_404.html')

    if not current_user.role == 'Admin':
        return render_template('page_401.html')

    form = MovieEditForm()
    form.category.choices, form.country.choices = get_choices(form)

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

            old_image = db.get_image(movie_key)
            if old_image:
                url = 'static/images/upload/movies/' + old_image
                os.remove(url)  # borrar la imagen anterior

        else:
            movie = Movie(title, year, category, country, None, stock, price)

        db.update_movie(movie_key, movie)

        return redirect(url_for('movie_page', movie_key=movie_key))

    form.title.data = movie.title
    form.year.data = movie.year
    form.category.data = str(movie.category)
    form.country.data = str(movie.country)
    form.stock.data = movie.stock
    form.price.data = movie.price

    return render_template('movie_edit.html', form=form)


@login_required
def categories():
    db = current_app.config['db']

    if not current_user.role == 'Admin':
        return render_template('page_401.html')

    form = CategoryForm()

    if form.validate_on_submit():
        category = form.data['category'].strip()
        cat = db.add_category(category)

        if cat:
            flash('Successfully added')
            return redirect(url_for('categories'))
        else:
            flash('Already exists')

    cat = db.get_categories()
    return render_template('category_edit.html', form=form, cat=cat)


@login_required
def delete_category(id_category):
    db = current_app.config['db']

    if not current_user.role == 'Admin':
        return render_template('page_401.html')

    db.delete_category(id_category)
    flash('Removed successfully')

    return redirect(url_for('categories'))


@login_required
def profile():
    return render_template('profile.html')


@login_required
def manage_users():
    if not current_user.role == 'Admin':
        return render_template('page_401.html')

    return render_template('manage_users.html')


def create_user():
    db = current_app.config['db']

    if not current_user.role == 'Admin':
        return render_template('page_401.html')

    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.data['username'].strip()  # Quitar espacios restantes
        password = form.data['password']
        hashed = hasher.hash(password)  # Contrase??a enmascarada

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

            image.save(os.path.join(current_app.config['UPLOAD_FOLDER_PROFILE'], filename))
            user = User(None, name, last_name, address, telephone if telephone else None, date_birth if date_birth else None, role, filename, username, hashed)
        else:
            user = User(None, name, last_name, address, telephone if telephone else None, date_birth if telephone else None, role, None, username, hashed)

        user_exists = db.get_user(username)

        if user_exists:
            flash('Nombre de usuario no disponible')
        else:
            db.create_user(user)
            return redirect(url_for('manage_users'))

    return render_template('user_edit.html', form=form)


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
    db = current_app.config['db']
    reports = db.report_sales()
    return render_template('report_sales.html', reports=reports)


def about():
    return render_template('about.html')


def get_choices(form):
    db = current_app.config['db']

    if form.category.choices:
        form.category.choices.clear()
        form.category.choices = db.get_categories()
    else:
        form.category.choices = db.get_categories()

    if form.country.choices:
        form.country.choices.clear()
        form.country.choices = db.get_countries()
    else:
        form.country.choices = db.get_countries()

    return form.category.choices, form.country.choices
