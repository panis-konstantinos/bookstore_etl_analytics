import requests
import bs4
import pandas as pd
import random

def get_book_refs():
    # Define a base url, page number, page flag and a titles list
    base_url = 'https://books.toscrape.com/catalogue/page-{}.html'
    page = 1
    active_page = True
    book_refs = []

    # Loop over all book pages
    while active_page:

        result = requests.get(base_url.format(page))
        if '404 Not Found' in result.text:
            # Mark loop flag as False if there is no other pages.
            print('Page not found. Quiting scrapping...')
            active_page = False

        else:
            # Scrap current page and get all book url references
            print(f'Scrapping page {page}...')
            soup = bs4.BeautifulSoup(result.text, 'lxml')
            page_books = soup.select('.product_pod')
            for book in page_books:
                href = book.select('a')[0]['href']
                book_refs.append(href)

            # Update page number
            page += 1

    return book_refs

def get_book_info(book_refs):
    # Define books url pattern, books and error list
    books_url = 'https://books.toscrape.com/catalogue/{}'
    books = []
    error_urls = []
    book_id = 1

    # Loop over every book title
    for book_ref in book_refs:

        # Get books HTML and scrap important data
        try:
            book_details_url = books_url.format(book_ref)
            print(f"Scrapping {book_details_url}...")
            result = requests.get(book_details_url)
            result.encoding = 'utf-8' # Define html encoding
            soup = bs4.BeautifulSoup(result.text, 'lxml')

            # Get useful html parts
            prod_main = soup.select('.col-sm-6.product_main')
            banner = soup.select('.breadcrumb')
            p_tag = soup.select('p')
            info_tab = soup.select('.table.table-striped')

            # Grab info needed using the specified html parts
            title = prod_main[0].select('h1')[0].text.strip()
            upc = info_tab[0].select('td')[0].text.strip()
            genre = banner[0].select('a')[2].text.strip()
            rating = prod_main[0].select('p')[2].get('class')[1] # Get the second word of class name (e.g. <p class="star-rating Three">)
            desc = p_tag[3].text
            price_excl_tax = info_tab[0].select('td')[2].text.strip()
            price_incl_tax = info_tab[0].select('td')[3].text.strip()
            tax = info_tab[0].select('td')[4].text.strip()
            stock = info_tab[0].select('td')[5].text.strip()
            reviews = info_tab[0].select('td')[6].text.strip()

            # Append books list with each book info
            book_info = [book_id, title, upc, genre, rating, desc, price_excl_tax, price_incl_tax, tax, stock, reviews]
            books.append(book_info)

            # Update book_id
            book_id += 1
            
        except Exception as error:
            # If an error occured, report error and add book's URL, book's title and index to error_urls list
            print(f"ERROR occured scrapping page {book_details_url}!\nError: {error}")
            error_urls.append([book_details_url, error])
    
    print(f"Gathered data for {len(books)} books.")
    print(f"Errors occured: {len(error_urls)}.")
    return books, error_urls

def create_books_df(books):
    # Define dataframe from books list
    df_books = pd.DataFrame(books, columns=["book_id", "title", "upc", "genre", "rating", "desc", 
                                            "price_excl_tax", "price_incl_tax", "tax", "stock", "reviews"])
    
    return df_books

def get_genres():
    # Grab all genres available
    result = requests.get('https://books.toscrape.com/index.html')
    print(f"Scrapping 'https://books.toscrape.com/index.html' for book genres...")
    soup = bs4.BeautifulSoup(result.text, 'lxml')
    nav_list = soup.select('.nav.nav-list a')

    genres = []
    for idx, category in enumerate(nav_list):
        if category.text.strip() != 'Books':
            genres.append([idx, category.text.strip()])
    
    print(f"{len(genres)} book genres found.")
    return genres

def create_genres_df(genres):
    df_genres = pd.DataFrame(genres, columns=['genre_id', 'genre'])
    return df_genres

def price_map(price):
  return float(price[1:])

def transform_df_books(df_books, df_genres):
    # Convert reviews stings to integer
    df_books['reviews'] = df_books['reviews'].astype(int)

    # Map rating literals to integer numbers
    rating_mapper = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    df_books['rating'] = df_books['rating'].map(lambda row: rating_mapper[row])

    # Convert price strings to float numbers
    df_books['price_excl_tax'] = df_books['price_excl_tax'].map(price_map)
    df_books['price_incl_tax'] = df_books['price_incl_tax'].map(price_map)
    df_books['tax'] = df_books['tax'].map(price_map)

    # Keep stock availability quantity
    df_books['stock'] = df_books['stock'].map(lambda stock: int(stock[10:12].strip()))

    # Map book genre to genre_id
    df_books['genre'] = df_books['genre'].map(lambda row: df_genres['genre_id'][df_genres['genre']== row].iloc[0])
    df_books.rename(columns={'genre': 'genre_id'}, inplace=True)

    return df_books

def create_synthetic_orders(df_books):
    # Create synthetic data for orders
    orders = []
    book_ids = df_books['book_id'].unique()

    # Create 50000 orders. Each order can have multiple books.
    for id in range(50000):

        # Random number of books for an order
        num_books = random.randint(1, 3)
        order_books = []

        # Random books selection
        for book in range(num_books):
            # Make sure that a book is not added more than once to an order
            book_id = random.choice(book_ids)
            while book_id in order_books:
                book_id = random.choice(book_ids)

            # Update current order books    
            order_books.append(book_id)
            
            # Random selection of book quantity
            quantity = random.randint(1, 4)

            # Add book to order
            orders.append([id + 1, int(book_id), quantity])
    
    return orders

def create_orders_df(orders):
    df_orders = pd.DataFrame(orders, columns=['order_id', 'book_id', 'quantity'])
    
    return df_orders

def save_dfs(df_books, df_genres, df_orders):
    df_books.to_pickle('./data/books.pkl')
    df_genres.to_pickle('./data/genres.pkl')
    df_orders.to_pickle('./data/orders.pkl')

def main():
    # Grab book references and book info. Then create book df
    book_refs = get_book_refs()
    books, error_urls = get_book_info(book_refs)
    df_books = create_books_df(books)

    # Grab book genres and create dataframe
    genres = get_genres()
    df_genres = create_genres_df(genres)

    # Transform book dataframe
    df_books = transform_df_books(df_books, df_genres)

    # Create synthetic orders data and orders dataframe
    orders = create_synthetic_orders(df_books)
    df_orders = create_orders_df(orders)

    # Save dataframes to pickle files
    save_dfs(df_books, df_genres, df_orders)


if __name__ == '__main__':
    main()