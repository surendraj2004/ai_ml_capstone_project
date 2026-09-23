import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import os
#loading dataset
df = sns.load_dataset("titanic")
print("\n Dataset loading successfully completed")
# create charts folder
os.makedirs("analytics/charts", exist_ok=True)
#basic data profile
print("=" * 30)
print("BASIC DATA PROFILE")
print("=" * 30)
print(df.head())
print("\n number of rows and columns:")
print(df.shape)
print("=" * 30)
print(" Dataset information")
print("=" * 30)
print(df.info())
print("=" * 30)
print("dataset description:")
print("=" * 30)
print(df.describe())
#missing values
print("=" * 30)
print("MISSING VALUES")
print("=" * 30)
missing_values = df.isna().sum()
missing_percentage = df.isna().mean() * 100

missing_values_table = pd.DataFrame({
    "missing_values_count" : missing_values,
    "missing_percentage" : missing_percentage
})
print(missing_values_table[missing_values_table["missing_values_count"]> 0])

#handling missing values
print("=" * 30)
print("HANDLING MISSING VALUES")
print("=" * 30)

# age column as more than 5% missing values
#  therefore impute with median()
age_missing_values = df["age"].isna().mean() * 100
print("age missing percentage:", age_missing_values)
df["age"] = df["age"].fillna(df["age"].median())

#embarked column has less than 5% missing values
# therefore droppping those rows
embarked_missing = df["embarked"].isna().mean() * 100
print("embarked missing values:", embarked_missing)
df = df.dropna(subset=["embarked"])
# deck has high percentage of missing values
# dropping the entire is preferable
deck_missing = df["deck"].isna().mean() * 100
print("deck missing percentage:", deck_missing)
df = df.drop(columns = ["deck"])

#checking after cleaning
print("=" * 30)
print(" cheking missing values after cleaning")
print("=" * 30)
print(df.isna().sum())

#fare mean medain mode
print("=" * 30)
print("FARE DISTRIBUTION")
print("=" * 30)
fare_mean = df["fare"].mean()
fare_median = df["fare"].median()
fare_mode = df["fare"].mode()[0]
print("fare mean", fare_mean)
print("fare median", fare_median)
print("fare mode", fare_mode)

print("\n fare skewness distribution:")
if fare_mean > fare_median > fare_mode:
    print("fare is right side skewed")
if fare_mean < fare_median < fare_mode:
    print("fare is left side skewed")
else:
    print("fare is approxmately symmetric")

#data visualization
print("=" * 30)
print("DATA VISUALIZATION")
print("=" * 30)
#Age Histogram
plt.figure(figsize= (8,5))
plt.hist(df["age"],bins = 20)
plt.xlabel("age")
plt.ylabel("number of passengers")
plt.title("age distribution")
plt.savefig("analytics/charts/age_histogram.png")
plt.show()
#Age Boxplot
plt.figure(figsize=(8,5))
plt.boxplot(df["age"])
plt.title("age boxplot")
plt.ylabel("age")
plt.savefig("analytics/charts/age_boxplot.png")
plt.show()
# Fare Histogram
plt.figure(figsize= (8,5))
plt.hist(df["fare"],bins = 20)
plt.xlabel("fare")
plt.ylabel("number of passengers")
plt.title("fare distribution")
plt.savefig("analytics/charts/fare_histogram.png")
plt.show()
#Fare Boxplot
plt.figure(figsize=(8,5))
plt.boxplot(df["fare"])
plt.title("fare boxplot")
plt.ylabel("fare")
plt.savefig("analytics/charts/fare_boxplot.png")
plt.show()
#IQR ouliers
print("=" * 30)
print(" IQR OUTLIERS")
print("=" * 30)
def find_outliers(column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3-q1
    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr
    outliers = df[
        (df[column] < lower_limit) |
        (df[column] > upper_limit)
    ]
    return len(outliers)
print("age outilers", find_outliers("age"))
print("fare outilers", find_outliers("fare"))
#survival rate by sex
print("=" * 30)
print("survival rate by sex")
print("=" * 30)
sex_survival = df.groupby("sex")["survived"].mean()
print(sex_survival)
#survival rate by pclass
print("=" * 30)
print("survival rate by passenger class")
print("=" * 30)
pclass_survival = df.groupby("pclass")["survived"].mean()
#survival rate by sex and pclass
print("=" * 30)
print("survival rate by sex and class")
print("=" * 30)
survival_sex_pclass = df.groupby(["sex","pclass"])["survived"].mean()
print(survival_sex_pclass)
#Boolean filtering
print("=" * 30)
print("Boolean filtering")
print("=" * 30)
#female survivers
female_survivars = df[
    (df["sex"] == "female") &
    (df["survived"] == 1)
]
print("\nfemale survivors")
print(female_survivars.head())
#firstclass survivors
firstclass_survivars = df[
    (df["pclass"] ==1) &
    (df["survived"] == 1)
]
print("\nfirst class survivars")
print(firstclass_survivars.head())

#correlation matrix
print("="* 30)
print(" Correlation matrix")
print("=" * 30)
correlation_columns = [
    "survived","pclass","sibsp","parch","age","fare"
]
correlation_matrix = df[correlation_columns].corr()
print(correlation_matrix)
#correlation heatmap
print("=" * 30)
print(" correlation heatmap")
print("=" * 30)
plt.figure(figsize=(8,6))
sns.heatmap(
    correlation_matrix,
    annot = True,
    cmap = "coolwarm"
)
plt.title("correlation heatmap")
plt.savefig("analytics/charts/titanic_heatmap.png")
plt.show()
 #two strongest correlations
print("\n two strongest correlations")
pairs = []
for column_1 in correlation_matrix.columns:

    for column_2 in correlation_matrix.columns:
        if column_1 != column_2:
            value = correlation_matrix.loc[column_1,column_2]
            pair = tuple(sorted([column_1, column_2]))
            pairs.append((pair,value))
pairs_df = pd.DataFrame(
    pairs,
    columns=["pairs","correlation"]
)
pairs_df["absolute"] = pairs_df["correlation"].abs()
pairs_df = pairs_df.drop_duplicates(subset=["pairs"])
strongest = pairs_df.sort_values(
    "absolute",
    ascending = False
).head(2)
print(strongest)

# multivaraite analysis
print("=" * 30)
print("multivaraite analysis")
print("=" * 30)
print("1.surival by sex")
plt.figure(figsize = (8,5))
sns.barplot(
    data = df,
x= "sex",
y="survived"
)
plt.title("survival rate by sex")
plt.savefig("analytics/charts/survival_by_sex.png")
plt.show()
print("\n2.survival by sex and class")
plt.figure(figsize=(8,5))
sns.barplot(
    data = df,
    x= "pclass",
    y = "survived",
    hue = "sex"
)
plt.title("survival rate by pclass and sex")
plt.savefig("analytics/charts/survival_pclass_sex.png")
plt.show()
print("\n 3.age and survival")
plt.figure(figsize = (8,5))
sns.boxplot(
    data = df,
    x= "survived",
    y="age"
)
plt.title("age distribution by survival")
plt.savefig("analytics/charts/age_survival_boxplot.png")
plt.show()
print("/n 4.fare and class by survival")
plt.figure(figsize=(8,5))
sns.boxplot(
    data = df,
    x = "pclass",
    y= "fare",
    hue = "survived"
)
plt.title("fare ,class and survival")
plt.savefig("analytics/charts/fare_class_survival_boxplot.png")
plt.show()

print("=" * 30)
print("STANDARDIZATION CHECK")
print("=" * 30)
scaler = StandardScaler()
df["age_standardized"] = scaler.fit_transform(df[["age"]])
df["fare_standardized"] = scaler.fit_transform(df[["fare"]])

print("\n original age")
print("mean", df["age"].mean())
print("std", df["age"].std())

print("\n standardized age")
print("mean", df["age_standardized"].mean())
print("std", df["age_standardized"].std())

print("\n original fare")
print("mean", df["fare"].mean())
print("std", df["fare"].std())

print("\n standardized fare")
print("mean", df["fare_standardized"].mean())
print("std", df["fare_standardized"].std())

#save data
df.to_csv("analytics/titanic_cleaned_data.csv",
index = False)

print("=" * 30)
print("EDA COMPLETED")
print("=" * 30)




