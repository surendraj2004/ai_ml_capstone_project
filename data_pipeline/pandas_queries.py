import pandas as pd
df = pd.read_csv("data_pipeline/cleaned_data.csv")
print(df.head())
#total number of books
print("\n total number of books")
print(len(df))
#books by category
print("\n books by category")
print(df["category"].value_counts())
#average price by category
print("\n average price by category")
print(df.groupby("category")["price_gbp"].mean())
#average rating by category
print("\n average rating by category")
print(df.groupby("category")["rating"].mean())
# check highest price
print("\n highest priced books")
print(df.sort_values("price_gbp",
ascending = False)
[["title","price_gbp", "category"]].head(10))
#highest rated books
print("\n highest rated books")
print(df.sort_values("rating",
ascending = False)
[["title", "rating","category"]].head(10))
#books that are in stock
print("\n books in stock")
print(df[df["in_stock"] == True].head(10))
#books that costs more than 40 pounds
print("\n books that costs more than 40 pounds")
print(df[df["price_gbp"] > 40][[
    "title", "price_gbp", "category"
]].head(10)
)
