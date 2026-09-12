import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import numpy as np
import pandas as pd

#website categories
categories = {
  "Business" : "https://books.toscrape.com/catalogue/category/books/business_35/index.html",
  "Mystery" : "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
  "Sequential_art" : "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"

}
#scraping through each category
all_books = []
for category_name, start_url in categories.items():
    print("\nscraping category", category_name)
    url = start_url
    while url:
        response = requests.get(url,timeout = 10)
        print("status code", response.status_code)
        soup = BeautifulSoup(response.text,"html.parser")
        books = soup.select("article.product_pod")
        print("books on this page", len(books))
        for book in books:
            title = book.h3.a["title"]
            price = book.select_one(".price_color").get_text(strip = True)
            rating = book.select_one(".star-rating")["class"][1]
            availability = book.select_one(".availability").get_text(" ", strip = True)
            #add books to list
            all_books.append({
                "title" : title,
                "price_gbp" : price,
                "rating" : rating,
                "availability" : availability,
                "category" : category_name
            })
        #check for next page
        next_page = soup.select_one("li.next a")
        if next_page:
            url = urljoin(url, next_page['href'])
        else:
            url = None 

#converting to dataframe
df = pd.DataFrame(all_books)

print("\n =============================")
print("scraping completed")
print(" =============================")
print("total books", len(df))
print("\n DataFrame shape")
print(df.shape)
print("\n first 5 rows")
print(df.head())

 #saving data to csv
df.to_csv("data_pipeline/raw_data.csv", index = False)
print("\n raw data saved successfully")
print("file: datapipeline/raw_data.csv")


                    


