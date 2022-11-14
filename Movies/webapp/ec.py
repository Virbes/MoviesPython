import os
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Movies.settings")

column = 'id_category'
table = 'Category'
args = '"Drama"'

with connection.cursor() as cursor:
    query = 'SELECT ' + column + ' FROM ' + table + ' WHERE ' + table + ' LIKE ' + args
    cursor.execute(query)
    data = cursor.fetchone()
    id, name = data
    print(id)
