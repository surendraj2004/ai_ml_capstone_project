import pandas as pd
import sqlite3
#loading cleaned data
df = pd.read_csv("data_pipeline/cleaned_data.csv")
# create sql database
connection = sqlite3.connect("data_base/books.db")
# create categories table
categories = pd.DataFrame({
    "category_id": [1, 2, 3],
    "category": ["Business", "Mystery", "Sequential_art"]
})
# save categories table
categories.to_sql(
    "categories",
    connection,
    if_exists="replace",
    index=False
)
# add category_id to books
df = df.merge(
    categories,
    on="category",
    how="left"
)
#creating books table
df.to_sql(
    "books",
    connection,
    if_exists= "replace",
    index = False
)
print("DataBase created succesfully")
# check categories table
print("\nCategories table:")
result = pd.read_sql(
    "SELECT * FROM categories",
    connection
)
print(result)
#check books table
result = pd.read_sql(
    "SELECT * FROM books LIMIT 5",
    connection
)
print("\n first 5 rows from database:")
print(result)
#total books
print("\n total number of  books:")
result = pd.read_sql(
    """ SELECT COUNT(*) AS total_books
    FROM books""",
    connection
)
print(result)
#books by category
print("\n books by category:")
result = pd.read_sql(
    """ SELECT category,
    COUNT(*) AS total_books
    FROM books
    GROUP BY category""",
    connection
)
print(result)
#average price by category
print("\n average price for category:")
result = pd.read_sql(
    """ SELECT category,
    AVG(price_gbp) AS average_price
    FROM books
    GROUP BY category""",
    connection
)
print(result)
#average rating by category
print("\n average rating by category:")
result = pd.read_sql(
    """ SELECT category,
    AVG(rating) AS average_rating
    FROM books
    GROUP BY category""",
    connection
)
print(result)
# highest price by category
print("highest price by category:")
result = pd.read_sql(
    """ SELECT title,price_gbp,category
    FROM books
    ORDER BY price_gbp DESC
    LIMIT 10""",
    connection
)
print(result)
#sql joins

#books with category details
print("\n books with category details")
result = pd.read_sql(
    """ SELECT books.title,
    books.price_gbp,
    books.category,
    categories.category_id
    FROM books
    JOIN categories
    ON books.category = categories.category
    LIMIT 10""",
    connection
)
print(result)

#close database
connection.close()
print("\n connection closed")
