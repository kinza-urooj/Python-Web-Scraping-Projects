import requests
from bs4 import BeautifulSoup
import pandas as pd

# Website URL
url = "https://quotes.toscrape.com/"

# Request website
response = requests.get(url)

print("Status Code:", response.status_code)

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Empty lists
quotes = []
authors = []
tags_list = []

# Find all quote containers
quote_boxes = soup.find_all("div", class_="quote")

# Extract data
for box in quote_boxes:

    quote = box.find("span", class_="text").text
    author = box.find("small", class_="author").text

    tags = box.find_all("a", class_="tag")
    tag_names = [tag.text for tag in tags]

    quotes.append(quote)
    authors.append(author)
    tags_list.append(", ".join(tag_names))

# Create DataFrame
df = pd.DataFrame({
    "Quote": quotes,
    "Author": authors,
    "Tags": tags_list
})

# Display data
print(df)

# Save CSV
df.to_csv("quotes_data.csv", index=False)

print("Quotes data saved successfully!")