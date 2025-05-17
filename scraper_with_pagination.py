import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Extract books from first page
url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
books = soup.find_all('h3')

for book in books:
    relative_url = book.find('a')['href']
    full_url = requests.compat.urljoin(url, relative_url)
    book_response = requests.get(full_url)
    book_soup = BeautifulSoup(book_response.content, "html.parser")

    title = book_soup.find('h1').text
    breadcrumb = book_soup.find('ul', class_="breadcrumb")
    if breadcrumb:
        category_links = breadcrumb.find_all('a')
        if len(category_links) >= 3:
            category = category_links[2].text.strip()
        else:
            category = "Category not found"
    else:
        category = "Breadcrumb not found"

    rating = book_soup.find('p', class_='star-rating')['class'][1]
    price = book_soup.find('p', class_='price_color').text.strip()
    availability = book_soup.find('p', class_='availability').text.strip()

    print(f'Title: {title}')
    print(f'Category: {category}')
    print(f'Rating: {rating}')
    print(f'Price: {price}')
    print(f'Availability: {availability}')
    print('************')


# Extract from all 50 pages
books_data = []

for page_num in range(1, 51):
    url = f'https://books.toscrape.com/catalogue/page-{page_num}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = soup.find_all('h3')

    for book in books:
        relative_url = book.find('a')['href']
        full_url = requests.compat.urljoin(url, relative_url)
        book_response = requests.get(full_url)
        book_soup = BeautifulSoup(book_response.content, "html.parser")

        title = book_soup.find('h1').text

        breadcrumb = book_soup.find('ul', class_="breadcrumb")
        if breadcrumb:
            category_links = breadcrumb.find_all('a')
            if len(category_links) >= 3:
                category = category_links[2].text.strip()
            else:
                category = "Category not found"
        else:
            category = "Breadcrumb not found"

        rating = book_soup.find('p', class_='star-rating')['class'][1]
        price = book_soup.find('p', class_='price_color').text.strip()
        availability = book_soup.find('p', class_='availability').text.strip()

        books_data.append([title, category, rating, price, availability])
        print(f'{len(books_data)} books extracted so far.....')

df = pd.DataFrame(books_data, columns=["Title", "Category", "Rating", "Price", "Availability"])
df.to_csv("books_scraped.csv", index=False)
print("Data saved in books_scraped.csv")
