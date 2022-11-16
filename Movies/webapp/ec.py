import os
from django.db import connection
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Movies.settings")

with connection.cursor() as cursor:
    query = 'SELECT * FROM Users WHERE Username LIKE %s'
    cursor.execute(query, ('Petaer',))

    user = cursor.fetchone()
    print(user)
