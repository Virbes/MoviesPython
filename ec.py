from sqlite3 import dbapi2


with dbapi2.connect('C:/Users/Francisco Virbes/Documents/PycharmProjects/pythonProject/movies.sqlite') as connection:
    cursor = connection.cursor()
    query = 'SELECT * FROM Users WHERE (Username LIKE ?)'
    cursor.execute(query, ('Admin',))
    print(cursor.fetchone())
