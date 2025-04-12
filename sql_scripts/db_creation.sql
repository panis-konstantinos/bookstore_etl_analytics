USE [MASTER]
GO

IF exists (SELECT * FROM sysdatabases WHERE NAME='Bookstore')
		DROP DATABASE Bookstore
GO

CREATE DATABASE [Bookstore]
GO

USE [Bookstore]
GO

CREATE TABLE Genres(
	genre_id INT NOT NULL PRIMARY KEY,
	genre VARCHAR(64)
	)

CREATE TABLE Books(
	book_id INT NOT NULL PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	upc VARCHAR(16) NOT NULL,
	genre_id INT NOT NULL,
	rating INT,
	descr TEXT,
	price_excl_tax FLOAT,
	price_incl_tax FLOAT,
	tax FLOAT,
	stock INT,
	reviews INT,
	FOREIGN KEY(genre_id) REFERENCES Genres(genre_id)
	)

CREATE TABLE Orders(
	order_id INT NOT NULL,
	book_id INT NOT NULL,
	quantity INT,
	PRIMARY KEY(order_id, book_id),
	FOREIGN KEY(book_id) REFERENCES Books(book_id)
	)