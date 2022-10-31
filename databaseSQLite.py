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
            query = 'SELECT * FROM Movies WHERE (id_movie = ?)'
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

            for img in cursor:
                image = img

            return image

    def get_user(self, username):
        with dbapi2.connect(self.db_file) as connection:

            cursor = connection.cursor()
            query = 'SELECT * FROM Users WHERE (Username = ?)'
            cursor.execute(query, (username,))

            for id_user, name, last_name, address, phone, date_birth, role, image, username, password in cursor:

                if id_user is not None:
                    user = User(id_user, name, last_name, address, phone, date_birth, role, image, username, password)

                return user

            else:
                return None

    def create_user(self, user):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            query = 'INSERT INTO Users(Name, LastName, Address, Phone, DateBirth, Role, Image, Username, Password) ' \
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(query, (user.name, user.last_name, user.address, user.phone, user.date_birth, user.role, user.image, user.username, user.password))

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
            query = 'INSERT INTO MOVIE(TITLE, YR) VALUES (?, ?)'
            cursor.execute(query, (movie.title, movie.year))
            connection.commit()
            movie_key = cursor.lastrowid
            print(movie_key, cursor.lastrowid)

        return movie_key

    def update_movie(self, movie_key, movie):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            query = 'UPDATE MOVIE SET TITLE = ?, YR = ? WHERE (ID = ?)'
            cursor.execute(query, (movie.title, movie.year, movie_key))
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
            cursor.execute('INSERT INTO Category(category) VALUES(?)', (category,))
            connection.commit()
            return True

    def delete_category(self, id_category):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM Category WHERE (id_category = ?)', (id_category,))
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
