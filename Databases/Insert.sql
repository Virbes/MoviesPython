INSERT INTO Category(category) VALUES('Terror'), ('Action'), ('Comedy'), ('Suspense'), ('Drama'), ('Documental');
INSERT INTO Country(country) VALUES('EEUU'), ('México'), ('España'), ('Italia'), ('Australia');
INSERT INTO Movies(Title, Year, Category, Country, Image, Stock, Price) VALUES('Toy Story 3', 2010, 1, 1, NULL, 10, 25);
INSERT INTO Payment_Method(payment_method) VALUES('Referencia Bancaria'), ('Efectivo'), ('Pago en línea');
INSERT INTO Users(Name, Role, Image, Username, Password) VALUES ('Administrator', 'Admin', 'admin.png', 'admin', '$pbkdf2-sha256$29000$PIdwDqH03hvjXAuhlLL2Pg$B1K8TX6Efq3GzvKlxDKIk4T7yJzIIzsuSegjZ6hAKLk');