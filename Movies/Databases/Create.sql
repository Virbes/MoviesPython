DROP DATABASE IF EXISTS movies;
CREATE DATABASE IF NOT EXISTS movies;

USE movies;

CREATE TABLE Category (
	id_category INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Category VARCHAR(30), 
    Status BOOLEAN DEFAULT TRUE
)ENGINE = InnoDB;

CREATE TABLE Country (
	id_country INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Country VARCHAR(30)
)ENGINE = InnoDB;

CREATE TABLE Movies (
	id_movie INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(30), 
    Year INT,
    Category INT,
    Country INT, 
    Image VARCHAR(150),
    
    Stock INT,
    Price INT,
    
    FOREIGN KEY (Category) REFERENCES Category(id_Category), 
    FOREIGN KEY (Country) REFERENCES Country(id_country)
)ENGINE = InnoDB;

CREATE TABLE Users (
	id_user INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
	Name VARCHAR(30), 
    LastName VARCHAR(30), 
    Address VARCHAR(50),
    Phone VARCHAR(15), 
    DateBirth Date, 
    Role VARCHAR(15), 
    Image VARCHAR(150),
    
    Username VARCHAR(30), 
    Password VARCHAR(150)
)ENGINE = InnoDB;

/**************************************************************/
CREATE TABLE My_Cart (
	id_cart INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    id_user INT NOT NULL, 
    id_movie INT NOT NULL, 
    acquisition_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_user) REFERENCES Users(id_user), 
    FOREIGN KEY (id_movie) REFERENCES Movies(id_movie)
)ENGINE = InnoDB;

CREATE TABLE Payment_Method (
	id_payment_method INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    payment_method VARCHAR(30)
)ENGINE = InnoDB;

CREATE TABLE Sales (
	id_sale INT NOT NULL PRIMARY KEY, 
    id_user INT NOT NULL, 
    total DOUBLE NOT NULL,
    id_payment_method INT NOT NULL, 
	sale_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_user) REFERENCES Users(id_user),
    FOREIGN KEY (id_payment_method) REFERENCES Payment_Method(id_payment_method)
)ENGINE = InnoDB;

CREATE TABLE Detail_Sale (
	id_sale INT NOT NULL,
	id_user INT NOT NULL, 
    id_movie INT NOT NULL, 
    precio_vendido DOUBLE NOT NULL,
    
    FOREIGN KEY (id_sale) REFERENCES Sales(id_sale),
    FOREIGN KEY (id_user) REFERENCES Users(id_user), 
    FOREIGN KEY (id_movie) REFERENCES Movies(id_movie)
)ENGINE = InnoDB;

