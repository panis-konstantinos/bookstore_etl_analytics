# About
This project is a data pipeline that scrapes data from a fictional bookstore website ([bookstoscrape.com](https://books.toscrape.com/)), processes the data, generates synthetic order data, and loads the data into an SQL Server database. The data is then analyzed using SQL queries, with the final output visualized using a Power BI report.

- **Web Scraping**: Utilized BeautifulSoup and Requests to scrape data from a fictional online bookstore ([bookstoscrape.com](https://books.toscrape.com/)).

- **Data Transformation**: Processed the scraped data by cleaning and organizing it into a structured format suitable for database storage.

- **Synthetic Order Data**: Generated synthetic order data to simulate real-world transactions.

- **SQL Server Integration**: Loaded the transformed and synthetic data into an SQL Server database using pyodbc module for further analysis.

- **SQL Analytics**: Performed analytics on the data by writing SQL queries and creating views to gain insights into sales, product availability, and more.

- **Power BI Reporting**: Developed an interactive Power BI report to visualize key metrics, such as top books (based on quantity sold and revenue), stock availabilty and books to promote (high rating, low sales).

# How to Run the Project
1. **Clone the Repository**
```
git clone https://github.com/panis-konstantinos/bookstore_etl_analytics.git
cd bookstore_etl_analytics
```

2. **Install the required dependencies**
```
pip install -r requirements.txt
```

3. Run **scrapper.py** to scrape the bookstore website, transform the gathered data and generate synthetic order data. You can also skip this step and proceed to step 4, as the data have already been saved in pickle files under the *data* folder.

4. Run *sql_scripts*/**db_creation.sql** to create database and tables in SQL Server.

5. Edit **config.example.json** by changing driver, server and database with your prefered driver (e.g. ODBC Driver 17 for SQL Server), and your server and database. After this you must rename the file as **config.json**. This file is crucial for connecting to your SQL Server using PyODBC module.

6. Run **load_db.py** to load data into SQL Server database.

7. Run *sql_scripts*/**analytics.sql** to generate insights from the database.

8. Run *sql_scripts*/**views.sql** to create views of data used in PowerBI.

9. Visualize the insights in file analytics_report.pdf under folder *PowerBI_report*
