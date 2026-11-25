import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time

# Starting website
url = "https://books.toscrape.com/"

# Create session
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

# Empty lists
book_names = []
prices = []
ratings = []
availability = []
book_links = []

# Counter
page_number = 1

# Scrape multiple pages
while url:

    print(f"Scraping page {page_number}...")

    # Send request
    response = session.get(url, timeout=20)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all books on current page
    books = soup.find_all("article", class_="product_pod")

    # Extract information
    for book in books:

        # Book name
        name = book.h3.a["title"]

        # Price
        price_text = book.find("p", class_="price_color").text.strip()
        price = float(price_text.replace("£", "").replace("Â", ""))

        # Rating
        rating = book.p["class"][1]

        # Availability
        stock = book.find("p", class_="instock availability").text.strip()

        # Book URL
        link = book.h3.a["href"]
        book_url = urljoin(url, link)

        # Add data to lists
        book_names.append(name)
        prices.append(price)
        ratings.append(rating)
        availability.append(stock)
        book_links.append(book_url)

    # Find next page
    next_button = soup.find("li", class_="next")

    if next_button:
        next_link = next_button.a["href"]
        url = urljoin(url, next_link)
        page_number += 1

        # Small delay to avoid sending requests too quickly
        time.sleep(0.3)

    else:
        url = None

# Create DataFrame
df = pd.DataFrame({
    "Book Name": book_names,
    "Price (£)": prices,
    "Rating": ratings,
    "Availability": availability,
    "Book URL": book_links
})

# Display summary
print("\nScraping completed!")
print("Total books collected:", len(df))
print("\nFirst 10 records:")
print(df.head(10))

# Save CSV
df.to_csv("big_books_dataset.csv", index=False, encoding="utf-8-sig")

# Save Excel
df.to_excel("big_books_dataset.xlsx", index=False)

print("\nCSV and Excel files saved successfully!")