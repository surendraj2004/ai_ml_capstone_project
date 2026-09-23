import pandas as pd
import sqlite3
import os

#loading cleaned data
df = pd.read_csv("data_pipeline/cleaned_data.csv")

#creating query results folder
os.makedirs("data_pipeline/query_results", exist_ok=True)

#create sql database
connection = sqlite3.connect("data_base/books.db")

#enable foreign key
connection.execute("PRAGMA foreign_keys = ON")

#creating categories table
connection.execute("""
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT UNIQUE
)
""")

#creating categories data
categories = pd.DataFrame({
    "category_id": [1, 2, 3],
    "category_name": ["Business", "Mystery", "Sequential_art"]
})

#saving categories table
categories.to_sql(
    "categories",
    connection,
    if_exists="append",
    index=False
)

#adding category id to books
df = df.merge(
    categories,
    left_on="category",
    right_on="category_name",
    how="left"
)

#creating book id
df.insert(
    0,
    "book_id",
    range(1, len(df) + 1)
)

#creating books table
connection.execute("""
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id)
    REFERENCES categories(category_id)
)
""")

#selecting required columns
books = df[
    [
        "book_id",
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category_id"
    ]
]

#converting true false into 1 and 0
books["in_stock"] = books["in_stock"].astype(int)

#saving books table
books.to_sql(
    "books",
    connection,
    if_exists="append",
    index=False
)

print("DataBase created succesfully")


#check categories table
print("\nCategories table:")

result = pd.read_sql(
    "SELECT * FROM categories",
    connection
)

print(result)


#check books table
print("\nFirst 5 rows from database:")

result = pd.read_sql(
    "SELECT * FROM books LIMIT 5",
    connection
)

print(result)


#query 1 - SELECT and WHERE
print("\nBooks with rating 4 or above:")

query1 = """
SELECT title, price_gbp, rating
FROM books
WHERE rating >= 4
"""

result = pd.read_sql(
    query1,
    connection
)

print(result)

result.to_csv(
    "data_pipeline/query_results/query1.csv",
    index=False
)


#query 2 - ORDER BY and LIMIT
print("\n10 highest priced books:")

query2 = """
SELECT title, price_gbp, rating
FROM books
ORDER BY price_gbp DESC
LIMIT 10
"""

result = pd.read_sql(
    query2,
    connection
)

print(result)

result.to_csv(
    "data_pipeline/query_results/query2.csv",
    index=False
)


#query 3 - DISTINCT
print("\nDifferent categories:")

query3 = """
SELECT DISTINCT category_name
FROM categories
"""

result = pd.read_sql(
    query3,
    connection
)

print(result)

result.to_csv(
    "data_pipeline/query_results/query3.csv",
    index=False
)


#query 4 - BETWEEN
print("\nBooks between 10 and 20 GBP:")

query4 = """
SELECT title, price_gbp, rating
FROM books
WHERE price_gbp BETWEEN 10 AND 20
"""

result = pd.read_sql(
    query4,
    connection
)

print(result)

result.to_csv(
    "data_pipeline/query_results/query4.csv",
    index=False
)


#query 5 - JOIN
print("\nBooks with category details:")

query5 = """
SELECT books.title,
       books.price_gbp,
       books.rating,
       categories.category_name
FROM books
JOIN categories
ON books.category_id = categories.category_id
LIMIT 10
"""

result = pd.read_sql(
    query5,
    connection
)

print(result)

result.to_csv(
    "data_pipeline/query_results/query5.csv",
    index=False
)


#reading query results using pd.read_sql
print("\nSQL join result:")

sql_result = pd.read_sql(
    query5,
    connection
)

print(sql_result)


#reproducing join using pd.merge
print("\nJoin using pd.merge:")

merge_result = pd.merge(
    books,
    categories,
    on="category_id",
    how="inner"
)

merge_result = merge_result[
    [
        "title",
        "price_gbp",
        "rating",
        "category_name"
    ]
].head(10)

print(merge_result)


#checking both results
print("\nAre both results same?")

print(
    sql_result.reset_index(drop=True).equals(
        merge_result.reset_index(drop=True)
    )
)


#close database
connection.close()

print("\nconnection closed")