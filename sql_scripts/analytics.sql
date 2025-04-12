USE Bookstore
GO

--Top 5 Books based on sales (quantity)
SELECT TOP 5 B.title, B.stock, SUM(O.quantity) AS Quantity_sold
FROM Books B, Orders O
WHERE B.book_id = O.book_id
GROUP BY B.title, B.stock
ORDER BY SUM(O.quantity) DESC;

--Bottom 5 books based on sales (quantity)
SELECT	TOP 5 B.title, B.stock, SUM(O.quantity) AS Quantity_sold
FROM Books B, Orders O
WHERE B.book_id = O.book_id
GROUP BY B.title, B.stock
ORDER BY SUM(O.quantity);

--Top 5 books based on revenue
SELECT TOP 5 B.title, B.stock, SUM(O.quantity * B.price_incl_tax) AS Total_revenue
FROM Books B, Orders O
WHERE B.book_id = O.book_id
GROUP BY B.title, B.stock
ORDER BY SUM(O.quantity * B.price_incl_tax);

--Top 5 genres based on quantity
SELECT G.genre, SUM(O.quantity) AS Quantity_sold
FROM Books B, Orders O, Genres G
WHERE B.book_id = O.book_id
  AND B.genre_id = G.genre_id
GROUP BY G.genre
ORDER BY SUM(O.quantity) DESC;

--Top 5 genres based on revenue
SELECT G.genre, ROUND(SUM(O.quantity * B.price_incl_tax), 2) AS Total_revenue
FROM Books B, Orders O, Genres G
WHERE B.book_id = O.book_id
  AND B.genre_id = G.genre_id
GROUP BY G.genre
ORDER BY ROUND(SUM(O.quantity * B.price_incl_tax), 2)  DESC;

--Available stock per genre
SELECT G.genre, SUM(B.stock) AS total_stock
FROM Books B, Genres G
WHERE B.genre_id = G.genre_id
GROUP BY G.genre
ORDER BY SUM(B.stock) DESC;

--Average book rating of available books by genre
SELECT G.genre, AVG(B.rating) AS Average_rating
FROM Books B, Genres G
WHERE B.genre_id = G.genre_id
GROUP BY G.genre
ORDER BY AVG(B.rating) DESC;

--Total books sold
SELECT SUM(O.quantity) AS Total_books_sold
FROM Orders O

--Total revenue
SELECT ROUND(SUM(O.quantity * B.price_incl_tax), 2) AS Total_revenue
FROM Books B, Orders O
WHERE B.book_id = O.book_id

--Average revenue per order
WITH OrdersRevenue AS (
	SELECT O.order_id, SUM(O.quantity * B.price_incl_tax) AS Order_revenue
	FROM Orders O, Books B
	WHERE O.book_id = B.book_id
	GROUP BY O.order_id
	)

SELECT ROUND(AVG(Order_revenue), 2) AS Average_order_revenue
FROM OrdersRevenue

--Available stock
SELECT SUM(B.stock) AS Total_stock
FROM Books B

--Top 10 High rating books with low sales
WITH Sales AS(
SELECT B.title, SUM(O.quantity) AS quantity_sold, ROUND(SUM(O.quantity * B.price_incl_tax), 2) AS total_revenue
FROM Books B, Orders O
WHERE B.book_id = O.book_id
GROUP BY B.title
)

SELECT TOP 10 B.title, B.rating, S.quantity_sold
FROM Sales S, Books B
WHERE S.title = B.title
  AND B.rating > 3
ORDER BY S.quantity_sold, B.title DESC;
