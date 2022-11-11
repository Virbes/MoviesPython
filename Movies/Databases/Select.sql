SELECT m.id_movie, m.Title, m.Year, ca.Category, co.Country, m.Image, m.Stock, m.Price
FROM Movies m, Category ca, Country co 
WHERE m.Category = ca.id_category AND m.Country = co.id_country;

select * from movies;
SELECT * FROM Users;
select * from category;
select * from country;
select * from my_cart;
select * from sales;
select * from detail_sale;
select * from payment_method;

SELECT id_cart, m.Title, acquisition_date, m.price FROM My_Cart c, Movies m WHERE c.id_movie = m.id_movie AND id_user = 2 ORDER BY id_cart;

SELECT detail.id_sale, movie.title, movie.image, detail.precio_vendido 
FROM Detail_Sale detail, Movies movie 
WHERE id_user = 1 AND detail.id_movie = movie.id_movie;

SELECT sale.id_sale, user.username, sale.total, payment.payment_method, sale.sale_date  
FROM sales sale, users user, payment_method payment
WHERE sale.id_user = user.id_user AND sale.id_payment_method = payment.id_payment_method
ORDER BY sale_date DESC;

select * from sales;

SELECT movie.Title, precio_vendido FROM detail_sale detail, Movies movie WHERE detail.id_movie = movie.id_movie AND id_sale = 48724;



