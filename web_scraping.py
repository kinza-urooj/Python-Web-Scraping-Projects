import requests
from bs4 import BeautifulSoup
import pandas as pd

# Website URL
url = "https://books.toscrape.com/"

# Send request to website
response = requests.get(url)

# Check website connection
print("Status Code:", response.status_code)

# Read HTML
soup = BeautifulSoup(response.text, "html.parser")

# Create empty lists
book_names = []
prices = []
ratings = []

# Find all books
books = soup.find_all("article", class_="product_pod")

# Extract information
for book in books:

    name = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    rating = book.p["class"][1]

    book_names.append(name)
    prices.append(price)
    ratings.append(rating)

# Create DataFrame
df = pd.DataFrame({
    "Book Name": book_names,
    "Price": prices,
    "Rating": ratings
})

# Display data
print(df)

# Save data to CSV
df.to_csv("scraped_books.csv", index=False)

print("\nData saved successfully!")