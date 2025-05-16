import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

books = soup.find_all("article", class_="product_pod")

data = []
for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text.strip()
    availability = book.find("p", class_="instock availability").text.strip()
    
    data.append({"Title": title, "Price": price, "Availability": availability})

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("books.csv", index=False)
print("Saved to books.csv")
