from random import randrange
from django.db import connection

from webapp.Pojo import Movie, User_Class


def get_movies():
    movies = []

    with connection.cursor() as cursor:
        query = 'SELECT id_movie, Title, Year, Image FROM Movies'
        cursor.execute(query)

        for _id, title, year, image in cursor:
            movies.append((_id, Movie(title, year, '', '', image, 0, 0)))

    return movies


def get_movie(movie_key):
    with connection.cursor() as cursor:
        query = 'SELECT m.id_movie, m.Title, m.Year, ca.Category, co.Country, m.Image, m.Stock, m.Price ' \
                'FROM Movies m, Category ca, Country co ' \
                'WHERE m.Category = ca.id_category AND m.Country= co.id_country AND id_movie = %s'
        cursor.execute(query, (movie_key,))

        data = cursor.fetchone()

        if data is not None:
            _id, title, year, category, country, image, stock, price = data
            return Movie(title, year, category, country, image, stock, price)

        return None


def get_id(table, column, args):
    with connection.cursor() as cursor:
        query = 'SELECT ' + column + ' FROM ' + table + ' WHERE ' + table + ' LIKE "' + args + '"'
        cursor.execute(query)
        data = cursor.fetchone()

        return data


def get_image(id_movie):
    with connection.cursor() as cursor:
        query = 'SELECT Image from Movies WHERE (id_movie = ?)'
        cursor.execute(query, (id_movie,))
        img = cursor.fetchone()[0]

        return img


def get_user(username):
    with connection.cursor() as cursor:
        query = 'SELECT * FROM Users WHERE Username LIKE %s'
        cursor.execute(query, (username,))

        user = cursor.fetchone()

        if user:
            id_user, name, last_name, address, phone, age, role, image, user_name, password = user
            return User_Class(id_user, name, last_name, phone, age, role, image, user_name, password)
        else:
            return None


def get_users():
    users_array = []

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Users')
        all_users = cursor.fetchall()

        for id_user, Name, LastName, Address, PhoneNumber, DateBirth, Role, Image, Username, Password in all_users:
            user = User_Class(id_user, Name, LastName, Address, PhoneNumber, DateBirth, Role, Image, Username, Password)

            users_array.append(user)

    return users_array


def create_user_db(user):
    with connection.cursor() as cursor:
        query = 'INSERT INTO Users(Name, LastName, Phone, Age, Role, Image, Username, Password) ' \
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (user.name, user.last_name,
                               user.phone, user.age, user.role,
                               user.image, user.username, user.password))

        connection.commit()


def delete_user_db(id_user):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM Users WHERE id_user = ?', (id_user,))
        connection.commit()


def update_user(user):
    with connection.cursor() as cursor:
        if user.image:
            query = 'UPDATE Users SET Name = ?, LastName = ?, PhoneNumber = ?, DateBirth = ?, Role = ?, Image = ? ' \
                    'WHERE Username = ?'
            values = (user.name, user.lastName, user.phoneNumber, user.dateBirth, user.role, user.image, user.username)

        else:
            query = 'UPDATE Users SET Name = ?, LastName = ?, PhoneNumber = ?, DateBirth = ?, Role = ? ' \
                     'WHERE Username = ?',
            values = (user.name, user.lastName, user.phoneNumber, user.dateBirth, user.role, user.username)

        cursor.execute(query, values)
        connection.commit()


def delete_movie(movie_key):
    with connection.cursor() as cursor:
        query = 'DELETE FROM MOVIES WHERE (id_movie = ?)'
        cursor.execute(query, (movie_key,))
        connection.commit()


def delete_my_movie_db(my_movie_key):
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_movie FROM My_Cart WHERE id_cart = ?', (my_movie_key,))
        id_movie = cursor.fetchone()

        cursor.execute('UPDATE Movies SET Stock = Stock+1 WHERE id_movie = ?', (id_movie['id_movie'],))
        cursor.execute('DELETE FROM My_Cart WHERE id_cart = ?', (my_movie_key,))
        connection.commit()


def add_movie(movie):
    with connection.cursor() as cursor:
        query = 'INSERT INTO Movies(Title, Year, Category, Country, Image, Stock, Price) ' \
                'VALUES(%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (movie.title, movie.year, movie.category, movie.country,
                               movie.image, movie.stock, movie.price))
        connection.commit()

        movie_key = cursor.lastrowid

    return movie_key


def update_movie(movie_key, movie):
    with connection.cursor() as cursor:
        if not movie.image:
            query = 'UPDATE Movies SET Title = %s, Year = %s, Category = %s, Country = %s, Stock = %s, Price = %s ' \
                    'WHERE id_movie = %s'
            cursor.execute(query, (movie.title, movie.year, movie.category, movie.country,
                                   movie.stock, movie.price, movie_key))
            connection.commit()
        else:
            query = 'UPDATE Movies SET Title=%s, Year=%s, Category=%s, Country=%s, Image=%s, Stock=%s, Price=%s ' \
                    'WHERE id_movie=%s'
            cursor.execute(query, (movie.title, movie.year, movie.category, movie.country, movie.image, movie.stock,
                                   movie.price, movie_key))
            connection.commit()


def get_categories():
    with connection.cursor() as cursor:
        categories = []
        query = 'SELECT * FROM Category'
        cursor.execute(query)

        for id_category, category, status in cursor:
            if status:
                categories.append((id_category, category))

        return categories


def add_category(category):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Category WHERE category LIKE %s', (category,))
        cat = cursor.fetchone()

        if cat:
            # Update Status Avalible
            if cat[2] == 0:
                cursor.execute('UPDATE Category SET Status = 1 WHERE id_category = %s', (cat[0],))
                connection.commit()
                return True

            # Already Exists Category
            return False
        else:
            cursor.execute('INSERT INTO Category(category) VALUES(%s)', (category,))
            connection.commit()
            return True


# This method not delete from BD but rather disables the visibility status
# so that there are no problems with records that depend on some -[CATEGORY]-.
def delete_category_db(id_category):
    with connection.cursor() as cursor:
        cursor.execute('UPDATE Category SET Status = %s WHERE id_category = %s', (0, id_category))
        connection.commit()


def get_countries():
    with connection.cursor() as cursor:
        countries = []
        cursor.execute('SELECT * FROM Country')

        for id_country, country in cursor:
            countries.append((id_country, country))

        return countries


def report_sales():
    with connection.cursor() as cursor:
        query = 'SELECT sale.id_sale, user.username, sale.total, payment.payment_method, sale.sale_date ' \
                'FROM sales sale, users user, payment_method payment ' \
                'WHERE sale.id_user = user.id_user AND sale.id_payment_method = payment.id_payment_method ' \
                'ORDER BY sale_date DESC'
        cursor.execute(query)


def add_movie_to_cart(id_user, id_movie):
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO My_Cart (id_user, id_movie ) VALUES (?, ?)', (id_user, id_movie))
        cursor.execute('UPDATE Movies SET Stock = Stock-1 WHERE id_movie = ?', (id_movie,))
        connection.commit()


def delete_all_my_movies(id_user):
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_movie FROM My_Cart WHERE id_user = ?', (id_user,))
        movies = cursor.fetchall()

        for movie in movies:
            cursor.execute('UPDATE Movies SET Stock = Stock+1 WHERE id_movie = ?', (movie['id_movie'],))
            connection.commit()

        cursor.execute('DELETE FROM My_Cart WHERE id_user = ?', (id_user,))
        connection.commit()


def get_my_cart(id_user):
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_cart, m.id_movie, m.title, acquisition_date, m.price, m.image '
                       'FROM My_Cart c, Movies m WHERE c.id_movie = m.id_movie '
                       'AND id_user = ? ORDER BY id_cart', (id_user,))
        my_movies = cursor.fetchall()

        return my_movies


def payment_cash(id_user, total):
    with connection.cursor() as cursor:
        cursor.execute('SELECT mc.id_movie, movie.price FROM My_Cart mc, movies movie '
                       'WHERE id_user = ? and movie.id_movie = mc.id_movie', (id_user,))
        my_movies = cursor.fetchall()

        id_sale = randrange(10000, 100000, 1)
        cursor.execute('INSERT INTO Sales(id_sale, id_user, total, id_payment_method) VALUES(?, ?, ?, ?)',
                       (id_sale, id_user, total, 2))
        connection.commit()

        for movie in my_movies:
            cursor.execute('INSERT INTO Detail_Sale(id_sale, id_user, id_movie, precio_vendido) '
                           'VALUES(?, ?, ?, ?)', (id_sale, id_user, movie.get('id_movie'), movie.get('price')))
            connection.commit()

        cursor.execute('DELETE FROM My_Cart WHERE id_user = ?', (id_user,))
        connection.commit()

        return id_sale


def get_ticket_items(id_sale, id_user):
    with connection.cursor() as cursor:
        cursor.execute('SELECT sale_date FROM Sales WHERE id_sale = ? AND id_user = ?', (id_sale, id_user))
        date_sale = cursor.fetchone()

        cursor.execute('SELECT movie.title, precio_vendido FROM detail_sale detail, Movies movie '
                       'WHERE detail.id_movie = movie.id_movie '
                       'AND id_sale = ? AND id_user = ?', (id_sale, id_user))
        items = cursor.fetchall()

        cursor.execute('SELECT SUM(precio_vendido) "total" FROM detail_sale '
                       'WHERE id_sale = ? AND id_user = ?', (id_sale, id_user))
        total = cursor.fetchone()

        return date_sale, items, total


def get_my_shopping(id_user):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Sales WHERE id_user = ? ORDER BY sale_date DESC', (id_user,))
        items = cursor.fetchall()

        return items


def get_detail_shopping(id_user):
    with connection.cursor() as cursor:
        cursor.execute('SELECT detail.id_sale, movie.title, movie.image, detail.precio_vendido '
                       'FROM Detail_Sale detail, Movies movie '
                       'WHERE id_user = ? AND detail.id_movie = movie.id_movie', (id_user,))
        details_shopping = cursor.fetchall()

        return details_shopping
