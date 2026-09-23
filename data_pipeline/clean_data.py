import pandas as pd

#import the original data
df = pd.read_csv("data_pipeline/raw_data.csv")

print("original data:")
print(df.head())

#cleaning the price column
df["price_gbp"] = (df['price_gbp'].str.replace("Â£", "", regex = False)
.str.replace("£", "", regex = False)
.str.strip()
)
#converting price to float
df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors = "coerce")
#convert rating column into numbers
rating_map ={
    "One" : 1,
    "Two" : 2,
    "Three" : 3,
    "Four": 4,
    "Five" : 5
}
df["rating"] = df["rating"].map(rating_map)
#converting availability into true\false
df["in_stock"] = df["availability"].str.strip() == "In stock"
#creating price in indian rupees 
df["price_inr"] = df["price_gbp"] * 105.50
#checking null values 
print("\n Missing Values:")
print(df.isna().sum())
#filling missing values
df["price_gbp"] = df["price_gbp"].fillna(df["price_gbp"].median())
df["rating"] = df["rating"].fillna(df["rating"].median())
#checking duplicate values
print("\n Duplicate values")
print(df.duplicated().sum())
#removing duplicate values
df = df.drop_duplicates()
#checking data types
print("\n data types")
print(df.dtypes)
print("\n data size")
print(df.shape)
print("\n column names")
print(df.columns.to_list())
#basic statistics
print("\ basic statistics:")
print("df.describe()")
#category count
print("\n books by category:")
print(df["category"].value_counts())
#average price by category in indain rupees
print("\n average price by category:")
print(df.groupby("category")["price_gbp"].mean())
#average rating by category
print("\n average rating of books by category:")
print(df.groupby("category")["rating"].mean())
# highest priced books
print("\n highest priced books")
print(df.sort_values("rating", ascending = False)
[["title", "price_gbp", "category"]].head(10))
#highest rated books
(print("\n highest rated books"))
print(df.sort_values("rating", ascending = False)
[["title","rating", "category"]].head(10))

#saving cleaned data
df.to_csv("data_pipeline/cleaned_data.csv", index = False)

print("\n cleaned data saved successfully")
print("file:data_pipeline/cleaned_data.csv")

print("\n cleaned data:")
print(df.head())

