import pandas as pd
import json
import pyodbc
import time

def read_files(books_path='./data/books.pkl', genres_path='./data/genres.pkl', orders_path='./data/orders.pkl'):
    df_books = pd.read_pickle(books_path)
    df_genres = pd.read_pickle(genres_path)
    df_orders = pd.read_pickle(orders_path)

    return df_books, df_genres, df_orders

def read_connection_config():
    with open("config.json") as f:
        config = json.load(f)

    driver = config["driver"]
    server = config["server"]
    db = config["database"]

    return driver, server, db

def create_connection(driver, server, db):
    conn_str = (f"DRIVER={driver};"
                f"SERVER={server};"
                f"DATABASE={db};"
                "Trusted_Connection=yes;")
    conn = pyodbc.connect(conn_str)

    return conn

def insert_genres(conn, df_genres):

    print("Inserting data to Genres table...")
    
    start = time.time()
    cursor = conn.cursor()
    cursor.fast_executemany = True

    query = f"INSERT INTO Genres(genre_id, genre) VALUES(?, ?)"
    cursor.executemany(query, df_genres.values.tolist())
    conn.commit()
    cursor.close()

    end = time.time()
    print(f"Succesfuly inserted {len(df_genres)} rows in {end - start:.4f} seconds.")

def insert_books(conn, df_books, chunk_size=10):
    print("Inserting data to Books table...")

    start = time.time()
    cursor = conn.cursor()
    cursor.fast_executemany = True

    # Define string of '?' for insert statement
    values_placeholders = ', '.join(['?' for _ in df_books.columns])

    # Insert data from df
    query = "INSERT INTO Books(book_id, title, upc, genre_id, rating, descr," \
    "                           price_excl_tax, price_incl_tax, tax, stock, reviews)" \
    f"       VALUES ({values_placeholders})"

    for i in range(0, len(df_books), chunk_size):
        chunk = df_books.iloc[i: i+chunk_size].values.tolist()
        cursor.executemany(query, chunk)
        conn.commit()
    cursor.close()

    end = time.time()
    print(f"Succesfuly inserted {len(df_books)} rows in {end - start:.4f} seconds.")

def insert_orders(conn, df_orders, chunk_size=6000):
    print("Inserting data to Orders table...")

    start = time.time()
    cursor = conn.cursor()
    cursor.fast_executemany = True

    # Insert data from df in chunks
    query = "INSERT INTO Orders(order_id, book_id, quantity) VALUES(?, ?, ?)"
    chunk = []
    for i in range(0, len(df_orders)):
        if len(chunk) < chunk_size and i < len(df_orders)-1:
            order = df_orders.iloc[i].values.tolist()
            chunk.append(order)
        else:
            # If chunk is filled, insert chunk and empty chunk.
            cursor.executemany(query, chunk)
            conn.commit()
            chunk = []
            order = df_orders.iloc[i].values.tolist()
            chunk.append(order)

    # Insert last chunk
    cursor.executemany(query, chunk)
    conn.commit()
    cursor.close()

    end = time.time()
    print(f"Succesfuly inserted {len(df_orders)} rows in {end - start:.4f} seconds.")

def main():
    # Load pickle files in dataframes
    df_books, df_genres, df_orders = read_files()

    # Connect to SQL Server
    driver, server, db = read_connection_config()
    conn = create_connection(driver, server, db)

    # Insert data to DB
    insert_genres(conn, df_genres)
    insert_books(conn, df_books)
    insert_orders(conn, df_orders)

    # Close connection
    conn.close()


if __name__ == '__main__':
    main()