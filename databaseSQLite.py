from user import User
from movie import Movie
import sqlite3 as dbapi2


class Database:

    def __init__(self, db_file):
        self.db_file = db_file

    def get_movies(self):
        movies = []

        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            query = 'SELECT id_movie, Title, Year, Image FROM Movies'
            cursor.execute(query)

            for _id, title, year, image in cursor:
                movies.append((_id, Movie(title, year, '', '', image, 0, 0)))

        return movies

    def get_movie(self, movie_key):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            query = 'SELECT m.id_movie, m.Title, m.Year, ca.Category, co.Country, m.Image, m.Stock, m.Price ' \
                    'FROM Movies m, Category ca, Country co ' \
                    'WHERE m.Category = ca.id_category AND m.Country= co.id_country AND id_movie = ?'
            cursor.execute(query, (movie_key,))

            data = cursor.fetchone()

            if data is not None:
                _id, title, year, category, country, image, stock, price = data
                return Movie(title, year, category, country, image, stock, price)

            return None

    def get_image(self, id_movie):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            query = 'SELECT Image from Movies WHERE (id_movie = ?)'
            cursor.execute(query, (id_movie,))
            img = cursor.fetchone()[0]

            return img

    def get_user(self, username):
        with dbapi2.connect(self.db_file) as connection:

            cursor = connection.cursor()
            query = 'SELECT * FROM Users WHERE (Username LIKE ?)'
            cursor.execute(query, (username,))

            user = cursor.fetchone()

            if user:
                id_user, name, last_name, address, phone, date_birth, role, image, user_name, password = user
                return User(id_user, name, last_name, address, phone, date_birth, role, image, user_name, password)
            else:
                return None

    def create_user(self, user):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            query = 'INSERT INTO Users(Name, LastName, Address, Phone, DateBirth, Role, Image, Username, Password) ' \
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(query, (user.name, user.last_name, user.address, user.phone, user.date_birth, user.role,
                                   user.image, user.username, user.password))

            connection.commit()

    def delete_movie(self, movie_key):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            query = 'DELETE FROM MOVIES WHERE (id_movie = ?)'
            cursor.execute(query, (movie_key,))
            connection.commit()

    def add_movie(self, movie):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            query = 'INSERT INTO Movies(Title, Year, Category, Country, Image, Stock, Price) ' \
                    'VALUES(?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(query, (movie.title, movie.year, movie.category, movie.country,
                                   movie.image, movie.stock, movie.price))
            connection.commit()

            movie_key = cursor.lastrowid

        return movie_key

    def update_movie(self, movie_key, movie):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()

            if not movie.image:
                query = 'UPDATE Movies SET Title = ?, Year = ?, Category = ?, Country = ?, Stock = ?, Price = ? ' \
                        'WHERE id_movie = ?'
                cursor.execute(query, (movie.title, movie.year, movie.category, movie.country,
                                       movie.stock, movie.price, movie_key))
                connection.commit()
            else:
                query = 'UPDATE Movies SET Title=?, Year=?, Category=?, Country=?, Image=?, Stock=?, Price=? ' \
                        'WHERE id_movie=?'
                cursor.execute(query, (movie.title, movie.year, movie.category, movie.country, movie.image, movie.stock,
                                       movie.price, movie_key))
                connection.commit()

    def get_categories(self):
        with dbapi2.connect(self.db_file) as connection:
            categories = []
            cursor = connection.cursor()
            query = 'SELECT * FROM Category'
            cursor.execute(query)

            for id_category, category, status in cursor:
                if status:
                    categories.append((id_category, category))

            return categories

    def add_category(self, category):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Category WHERE category LIKE ?', (category,))
            cat = cursor.fetchone()

            if cat:
                # Update Status Avalible
                if cat[2] == 0:
                    cursor.execute('UPDATE Category SET Status = 1 WHERE id_category = ?', (cat[0],))
                    connection.commit()
                    return True

                # Already Exists Category
                return False
            else:
                cursor.execute('INSERT INTO Category(category) VALUES(?)', (category,))
                connection.commit()
                return True

    # This method not delete from BD but rather disables the visibility status
    # so that there are no problems with records that depend on some -[CATEGORY]-.
    def delete_category(self, id_category):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            cursor.execute('UPDATE Category SET Status = ? WHERE id_category = ?', (0, id_category))
            connection.commit()

    def get_countries(self):
        with dbapi2.connect(self.db_file) as connection:
            countries = []

            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Country')

            for id_country, country in cursor:
                countries.append((id_country, country))

            return countries

    def report_sales(self):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            query = 'SELECT sale.id_sale, user.username, sale.total, payment.payment_method, sale.sale_date ' \
                    'FROM sales sale, users user, payment_method payment ' \
                    'WHERE sale.id_user = user.id_user AND sale.id_payment_method = payment.id_payment_method ' \
                    'ORDER BY sale_date DESC'
            cursor.execute(query)
