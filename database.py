from random import randrange

import mysql.connector
from flask import current_app
from movie import Movie
from user import User


def get_movies():
    movies = []
    db, c = get_db()

    c.execute('SELECT id_movie, Title, Year FROM Movies')
    all_movies = c.fetchall()

    for movie in all_movies:
        movie_key = movie.get('id_movie')
        title = movie.get('Title')
        year = movie.get('Year')

        movies.append((movie_key, Movie(title, year, '', '', '', 0, 0)))

    return movies


def get_movie(id):
    db, c = get_db()

    c.execute('SELECT m.id_movie, m.Title, m.Year, ca.Category, co.Country, m.Image, m.Stock, m.Price FROM Movies m, Category ca, Country co WHERE m.Category = ca.id_category AND m.Country = co.id_country AND id_movie = %s', (id,))
    movie = c.fetchone()

    if movie:
        title = movie.get('Title')
        year = movie.get('Year')
        category = movie.get('Category')
        country = movie.get('Country')
        image = movie.get('Image')
        stock = movie.get('Stock')
        price = movie.get('Price')

        return Movie(title, year, category, country, image, stock, price)

    return None


def add_movie(movie):
    db, c = get_db()

    c.execute('INSERT INTO Movies(Title, Year, Category, Country, Image, Stock, Price) VALUES(%s, %s, %s, %s, %s, %s, %s)',
              (movie.title, movie.year, movie.category, movie.country, movie.image, movie.stock, movie.price))
    db.commit()

    c.execute('SELECT id_movie FROM Movies WHERE Title = %s', (movie.title,))
    movie_key = c.fetchone()

    return movie_key.get('id_movie')


def update_movie(movie_key, movie):
    db, c = get_db()

    if not movie.image:
        c.execute('UPDATE Movies SET Title = %s, Year = %s, Category = %s, Country = %s, Stock = %s, Price = %s WHERE id_movie = %s',
                  (movie.title, movie.year, movie.category, movie.country, movie.stock, movie.price, movie_key))
    else:
        c.execute('UPDATE Movies SET Title = %s, Year = %s, Category = %s, Country = %s, Image = %s, Stock = %s, Price = %s WHERE id_movie = %s',
                  (movie.title, movie.year, movie.category, movie.country, movie.image, movie.stock, movie.price, movie_key))

    db.commit()


def delete_movie(movie_key):
    db, c = get_db()

    c.execute('DELETE FROM Movies WHERE id_movie = %s', (movie_key,))
    db.commit()


def get_my_cart(id_user):
    db, c = get_db()

    c.execute('SELECT id_cart, m.id_movie, m.title, acquisition_date, m.price, m.image FROM My_Cart c, Movies m WHERE c.id_movie = m.id_movie AND id_user = %s ORDER BY id_cart', (id_user,))
    my_movies = c.fetchall()
    return my_movies


def delete_my_movie(my_movie_key):
    db, c = get_db()

    c.execute('SELECT id_movie FROM My_Cart WHERE id_cart = %s', (my_movie_key,))
    id_movie = c.fetchone()

    c.execute('UPDATE Movies SET Stock = Stock+1 WHERE id_movie = %s', (id_movie['id_movie'],))
    c.execute('DELETE FROM My_Cart WHERE id_cart = %s', (my_movie_key,))
    db.commit()


def delete_all_my_movies(id_user):
    db, c = get_db()

    c.execute('SELECT id_movie FROM My_Cart WHERE id_user = %s', (id_user,))
    movies = c.fetchall()

    for movie in movies:
        c.execute('UPDATE Movies SET Stock = Stock+1 WHERE id_movie = %s', (movie['id_movie'],))
        db.commit()

    c.execute('DELETE FROM My_Cart WHERE id_user = %s', (id_user,))
    db.commit()


def get_categories():
    db, c = get_db()

    categories = []

    c.execute('SELECT * FROM Category')
    all_categories = c.fetchall()

    for category in all_categories:
        if category.get('Status'):
            categories.append((category.get('id_category'), category.get('Category')))

    return categories


def add_category(category):
    db, c = get_db()

    c.execute('SELECT * FROM Category WHERE category = %s', (category,))
    cat = c.fetchone()

    if cat is None:
        c.execute('INSERT INTO Category(category) VALUES(%s)', (category,))
        db.commit()
        return True
    elif cat['status'] == 0:
        c.execute('UPDATE Category set status = 1 where id_category = %s', (cat['id_category'],))
        db.commit()
        return True
    else:
        return False


def delete_category(id_category):
    db, c = get_db()

    c.execute('UPDATE Category SET status = false WHERE id_category = %s', (id_category,))
    db.commit()


def get_countries():
    db, c = get_db()

    countries = []

    c.execute('SELECT * FROM Country')
    all_country = c.fetchall()

    for country in all_country:
        countries.append((country.get('id_country'), country.get('Country')))

    return countries


def get_image(id_movie):
    db, c = get_db()

    c.execute('SELECT Image from Movies WHERE id_movie = %s', (id_movie,))
    img = c.fetchone()

    return img.get('Image')


def get_users():
    db, c = get_db()
    users = []

    c.execute('SELECT * FROM Users')
    all_users = c.fetchall()

    for user in all_users:
        u = User(user.get('id_user'), user.get('Name'), user.get('LastName'), user.get('Address'), user.get('PhoneNumber'), user.get('DateBirth'),
                 user.get('Role'), user.get('Image'), user.get('Username'), user.get('Password'))

        users.append(u)

    return users


def get_user(username):
    db, c = get_db()

    c.execute('SELECT * FROM Users WHERE Username = %s', (username,))
    user = c.fetchone()

    if user is not None:
        id_user = user.get('id_user')
        name = user.get('Name')
        lastName = user.get('LastName')
        address = user.get('Address')
        phone = user.get('Phone')
        dateBirth = user.get('DateBirth')
        role = user.get('Role')
        image = user.get('Image')
        password = user.get('Password')

        user = User(id_user, name, lastName, address, phone, dateBirth, role, image, username, password)

        if user is not None:
            user.is_admin = role in current_app.config['ADMIN_USERS']

        return user

    else:
        return None


def create_user(user):
    db, c = get_db()

    c.execute(
        'INSERT INTO Users(Name, LastName, Address, Phone, DateBirth, Role, Image, Username, Password) '
        'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (user.name, user.lastName, user.address, user.phone, user.dateBirth, user.role, user.image, user.username, user.password))

    db.commit()


def update_user(user):
    db, c = get_db()

    if user.image:
        c.execute(
            'UPDATE Users SET Name = %s, LastName = %s, PhoneNumber = %s, DateBirth = %s, Role = %s, Image = %s WHERE Username = %s',
            (user.name, user.lastName, user.phoneNumber, user.dateBirth, user.role, user.image, user.username))
        db.commit()
    else:
        c.execute(
            'UPDATE Users SET Name = %s, LastName = %s, PhoneNumber = %s, DateBirth = %s, Role = %s WHERE Username = %s',
            (user.name, user.lastName, user.phoneNumber, user.dateBirth, user.role, user.username))
        db.commit()


def delete_user(id_user):
    db, c = get_db()

    c.execute('DELETE FROM Users WHERE id_user = %s', (id_user,))
    db.commit()


def add_movie_to_cart(id_user, id_movie):
    db, c = get_db()

    c.execute('INSERT INTO My_Cart (id_user, id_movie ) VALUES (%s, %s)', (id_user, id_movie))
    c.execute('UPDATE Movies SET Stock = Stock-1 WHERE id_movie = %s', (id_movie,))
    db.commit()


def get_payment_methods():
    db, c = get_db()
    payments = []

    c.execute('SELECT * FROM Payment_Method')
    all_payments = c.fetchall()

    for payment in all_payments:
        payments.append(payment)

    return payments


def payment_cash(id_user, total):
    db, c = get_db()

    c.execute('SELECT mc.id_movie, movie.price FROM My_Cart mc, movies movie WHERE id_user = %s and movie.id_movie = mc.id_movie', (id_user,))
    my_movies = c.fetchall()

    id_sale = randrange(10000, 100000, 1)
    c.execute('INSERT INTO Sales(id_sale, id_user, total, id_payment_method) VALUES(%s, %s, %s, %s)', (id_sale, id_user, total, 2))
    db.commit()

    for movie in my_movies:
        c.execute('INSERT INTO Detail_Sale(id_sale, id_user, id_movie, precio_vendido) VALUES(%s, %s, %s, %s)', (id_sale, id_user, movie.get('id_movie'), movie.get('price')))
        db.commit()

    c.execute('DELETE FROM My_Cart WHERE id_user = %s', (id_user,))
    db.commit()

    return id_sale


def report_sales():
    db, c = get_db()

    c.execute('SELECT sale.id_sale, user.username, sale.total, payment.payment_method, sale.sale_date FROM sales sale, users user, payment_method payment WHERE sale.id_user = user.id_user AND sale.id_payment_method = payment.id_payment_method ORDER BY sale_date DESC')
    report = c.fetchall()

    return report


def get_my_shopping(id_user):
    db, c = get_db()

    c.execute('SELECT * FROM Sales WHERE id_user = %s ORDER BY sale_date DESC', (id_user,))
    items = c.fetchall()

    return items


def get_detail_shopping(id_user):
    db, c = get_db()

    c.execute('SELECT detail.id_sale, movie.title, movie.image, detail.precio_vendido FROM Detail_Sale detail, Movies movie WHERE id_user = %s AND detail.id_movie = movie.id_movie', (id_user,))
    details_shopping = c.fetchall()

    return details_shopping


def get_ticket_items(id_sale, id_user):
    db, c = get_db()

    c.execute('SELECT sale_date FROM Sales WHERE id_sale = %s AND id_user = %s', (id_sale, id_user))
    date_sale = c.fetchone()

    c.execute('SELECT movie.title, precio_vendido FROM detail_sale detail, Movies movie WHERE detail.id_movie = movie.id_movie AND id_sale = %s AND id_user = %s', (id_sale, id_user))
    items = c.fetchall()

    c.execute('SELECT SUM(precio_vendido) "total" FROM detail_sale WHERE id_sale = %s AND id_user =%s', (id_sale, id_user))
    total = c.fetchone()

    return date_sale, items, total


# Connection to MySQL
def get_db():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='Movies'
    )
    c = db.cursor(dictionary=True)
    return db, c
