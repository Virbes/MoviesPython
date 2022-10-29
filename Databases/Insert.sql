INSERT INTO Category(category) VALUES('Terror'), ('Action'), ('Comedy'), ('Suspense'), ('Drama'), ('Documental');
INSERT INTO Country(country) VALUES('EEUU'), ('México'), ('España'), ('Italia'), ('Australia');
INSERT INTO movies (id_movie, Title, Year, Category, Country, Image, Stock, Price) VALUES
(1, 'Game of Thrones', 1887, 1, 1, 'Game of Thrones20221018014653.jpg', 19, 500),
(2, 'Anabelle', 1887, 1, 1, 'Anabelle20221018210536.jpg', 0, 1),
(3, 'Avengers', 1887, 1, 1, 'Avengers20221018210555.jpg', 0, 1),
(4, 'Django', 1887, 1, 1, 'Django20221018210612.jpg', 0, 1),
(5, 'Joker', 1887, 1, 1, 'Joker20221018210638.jpg', 1, 1);
INSERT INTO Payment_Method(payment_method) VALUES('Referencia Bancaria'), ('Efectivo'), ('Pago en línea');
INSERT INTO Users(Name, Role, Image, Username, Password) VALUES ('Administrator', 'Admin', 'admin.png', 'admin', '$pbkdf2-sha256$29000$PIdwDqH03hvjXAuhlLL2Pg$B1K8TX6Efq3GzvKlxDKIk4T7yJzIIzsuSegjZ6hAKLk');