#  Data Pipeline

## Project Overview

This project collects books data from the Books to Scrape website and processes the data using Python, Pandas, and SQLite.

## Installation

Create and activate a Python virtual environment.

Install the required libraries:

    pip install requests beautifulsoup4 pandas numpy

## How to Run

Run the scraper:

    python data_pipeline/scraper.py

Run the data cleaning script:

    python data_pipeline/clean_data.py

Run the database script:

    python data_pipeline/database.py

Run the Pandas analysis:

    python data_pipeline/pandas_queries.py

## Scraping Decisions

The Books to Scrape website was used as the data source.

Books were collected from three categories:

- Business
- Mystery
- Sequential_art

The scraper follows the next-page link to collect books from all available pages in each selected category.

The following information was collected:

- Book title
- Price
- Rating
- Availability
- Category

## Cleaning Decisions

The price was cleaned by removing the pound symbol and converting the value to a numeric data type.

Book ratings such as One, Two, Three, Four, and Five were converted into numbers from 1 to 5.

Availability was converted into a Boolean value:

- In stock = True
- Not in stock = False

Duplicate records and missing values were checked.

## Currency Conversion

The fixed conversion rate used in this project is:

1 GBP = 129.28 INR

The INR price was calculated using:

price_inr = price_gbp * 129.28

## Database Design

SQLite was used to store the cleaned book data.

The database contains two tables:

- books
- categories

The categories table contains category information and category IDs.

The books table contains book information and category information.

A SQL JOIN was used to combine information from the books and categories tables.

## SQL Analysis

SQL queries were used to analyze the data, including:

- Total number of books
- Number of books by category
- Average price by category
- Average rating by category
- Highest-priced books
- JOIN between books and categories

Pandas was also used to reproduce analysis and JOIN operations.

## Output Files

The pipeline generates:

- raw_data.csv
- cleaned_data.csv
- books.db