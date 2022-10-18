from database import get_db

db, c = get_db()

c.execute('SELECT sale_date FROM Sales WHERE id_sale = %s AND id_user = %s', (48724, 1))
date_sale = c.fetchone()

print(date_sale)