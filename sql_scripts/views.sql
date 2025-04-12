USE Bookstore
GO

--Book sales based on quantity and revenue
CREATE VIEW BookSales AS
SELECT B.title, B.stock, SUM(O.quantity) AS quantity_sold, ROUND(SUM(O.quantity * B.price_incl_tax), 2) AS total_revenue
FROM Books B, Orders O
WHERE B.book_id = O.book_id
GROUP BY B.title, B.stock;
GO

--Genre sales based on quantity and revenue
CREATE VIEW GenreSales AS
SELECT G.genre, SUM(O.quantity) AS quantity_sold, ROUND(SUM(O.quantity * B.price_incl_tax), 2) AS total_revenue
FROM Books B, Orders O, Genres G
WHERE B.book_id = O.book_id
  AND B.genre_id = G.genre_id
GROUP BY G.genre;
GO

--Average book rating of available books by genre
CREATE VIEW GenreRatings AS
SELECT G.genre, AVG(B.rating) AS average_rating
FROM Books B, Genres G
WHERE B.genre_id = G.genre_id
GROUP BY G.genre;
GO

--Average revenue per order
CREATE VIEW AvgRevenueOrder AS
SELECT ROUND(AVG(OrderRev.Order_revenue), 2) AS average_order_revenue
FROM (
	SELECT O.order_id, SUM(O.quantity * B.price_incl_tax) AS order_revenue
	FROM Orders O, Books B
	WHERE O.book_id = B.book_id
	GROUP BY O.order_id
	) AS OrderRev
GO 

--Available stock per genre
CREATE VIEW GenreStocks AS
SELECT G.genre, SUM(B.stock) AS total_stock
FROM Books B, Genres G
WHERE B.genre_id = G.genre_id
GROUP BY G.genre
GO

--Top 10 books with high rating but low sales
CREATE VIEW HighRating_LowSales AS
SELECT TOP 10 B.title, B.rating, BS.quantity_sold
FROM BookSales BS, Books B
WHERE BS.title = B.title
  AND B.rating > 3
ORDER BY BS.quantity_sold