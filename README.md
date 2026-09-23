# Capstone Project

This repository contains my capstone project developed as part of my learning journey in Artificial Intelligence (AI), Machine Learning (ML), Data Analytics, and related technologies.

As a fresher, this project helps me apply the concepts and tools I have learned through practical implementation across data analytics, machine learning, and AI application development.

---

## Project Modules

### 1. Data Pipeline

This module focuses on building an end-to-end data pipeline.

It includes:

- Data collection through web scraping
- Data cleaning
- Data transformation
- SQLite database operations
- SQL queries and analysis
- Pandas-based data analysis

### 2. Analytics & Machine Learning

This module focuses on exploratory data analysis and machine learning using the Titanic dataset.

It includes:

- Exploratory Data Analysis (EDA)
- Data cleaning and preprocessing
- Data visualization
- Correlation analysis
- Feature standardization
- Classification models
- Class imbalance handling
- Random Forest tuning
- Regression
- Model evaluation
- Model pipeline saving using Joblib

### 3. Support Assistant

This module focuses on building an AI-powered customer support assistant for Zepto.

It includes:

- Policy document ingestion
- Text chunking
- Sentence Transformer embeddings
- ChromaDB vector database
- Semantic retrieval
- LangGraph workflow
- Prompt engineering
- Pydantic response validation
- FastAPI API
- Docker deployment
- Mock LLM mode

---

# Project Structure

```text
capstone_project/
│
├── README.md
│
├── data_pipeline/
│   │
│   ├── raw_data.csv
│   ├── cleaned_data.csv
│   │
│   ├── scraper.py
│   ├── clean_data.py
│   ├── database.py
│   ├── pandas_queries.py
│   │
│   └── query_results/
│
│
├── analytics/
│   │
│   ├── titanic_cleaned_data.csv
│   │
│   ├── EDA_analysis.py
│   ├── model_traning.py
│   ├── titanic_pipeline.joblib
│   │
│   ├── models/
│   │
│   └── outputs/
│
│
└── support_assistant/
    │
    ├── docs/
    │   │
    │   ├── doc_01_delivery.txt
    │   ├── doc_02_returns_refunds.txt
    │   ├── doc_03_membership.txt
    │   ├── doc_04_tracking.txt
    │   ├── doc_05_cancellation.txt
    │   ├── doc_06_damaged_missing.txt
    │   ├── doc_07_gift_cards.txt
    │   └── doc_08_support.txt
    │
    ├── chroma_db/
    │
    ├── ingest.py
    ├── graph.py
    ├── prompts.py
    ├── models.py
    ├── main.py
    ├── Dockerfile
    └── README.md


    Module 1 — Data Pipeline
Objective

The Data Pipeline module collects book data from books.toscrape.com, cleans the collected data, stores the data in a SQLite database, and performs SQL analysis.

Workflow
Books to Scrape
       │
       ▼
   scraper.py
       │
       ▼
 raw_data.csv
       │
       ▼
 clean_data.py
       │
       ▼
cleaned_data.csv
       │
       ▼
 database.py
       │
       ▼
 SQLite Database
       │
       ▼
pandas_queries.py
       │
       ▼
 Query Results
Data Collected

The pipeline collects:

Book title
Price in GBP
Star rating
Availability
Category
Data Cleaning

The cleaning process includes:

Removing currency symbols
Converting price into numeric format
Converting star ratings into numerical values from 1 to 5
Converting availability into a boolean in_stock field
Handling missing numeric values
Removing duplicate records
Calculating price in INR

The fixed conversion rate used is:

1 GBP = 105.50 INR

The cleaned data is stored in:

data_pipeline/cleaned_data.csv
Database

The cleaned data is stored in SQLite using a normalized relational structure.

The database contains related tables using primary-key and foreign-key relationships.

SQL Analysis

The project performs SQL analysis using queries covering:

SELECT
WHERE
ORDER BY
LIMIT
DISTINCT
IN
BETWEEN
JOIN

Query outputs are stored in:

data_pipeline/pandas_queries.py/

The project also demonstrates reading SQL results using Pandas and reproducing equivalent join operations using Pandas.

Module 2 — Analytics & Machine Learning
Objective

The Analytics module performs exploratory data analysis and machine learning using the Titanic dataset.

Workflow
Titanic Dataset
       │
       ▼
EDA Analysis
       │
       ▼
Data Cleaning
       │
       ▼
Preprocessing
       │
       ├───────────────┐
       ▼               ▼
 Classification     Regression
       │               │
       ▼               ▼
 Model Evaluation   Model Evaluation
Dataset

The Titanic dataset is processed and stored as:

analytics/titanic_cleaned_data.csv
Exploratory Data Analysis

The analysis includes:

Dataset shape
Dataset information
Descriptive statistics
Missing-value analysis
Missing-value treatment
Age distribution
Fare distribution
Box plots
IQR-based outlier analysis
Fare mean
Fare median
Fare mode
Fare skewness
Survival analysis by sex
Survival analysis by passenger class
Survival analysis by sex and passenger class
Correlation analysis
Multivariate visualizations

The correlation analysis uses:

survived
pclass
age
sibsp
parch
fare

A correlation heatmap is also included.

Feature Standardization

The age and fare features are standardized and their statistics are compared before and after standardization.

Classification

The project implements three classification algorithms:

Logistic Regression
Decision Tree
Random Forest

The classification workflow includes:

Stratified train/test split
Missing-value imputation
Categorical encoding
Numerical scaling
Model training
Model evaluation
Evaluation Metrics

The classification models are evaluated using:

Accuracy
Precision
Recall
F1-score
Confusion Matrix
ROC Curve
AUC
Class Imbalance

The project evaluates different approaches to class imbalance:

Baseline model
Balanced class weights
SMOTE

SMOTE is applied only to the training data.

Random Forest Tuning

Random Forest hyperparameters are optimized using GridSearchCV.

The search includes:

n_estimators
max_depth
max_features

The Random Forest model uses:

oob_score=True

The best parameters and OOB score are reported.

Regression

A regression model is developed to predict fare using other available features.

The regression model is evaluated using:

MAE
RMSE
R²
Adjusted R²

A residual plot is used to analyze the regression errors and discuss potential heteroscedasticity.

Model Pipeline

The final machine learning pipeline is saved using Joblib:

analytics/titanic_pipeline.joblib

The saved pipeline can be loaded again for prediction.

Module 3 — Support Assistant
Objective

The Support Assistant is an AI-powered customer support application designed to answer questions using a Zepto policy knowledge base.

The application uses a Retrieval-Augmented Generation (RAG) approach.

Architecture
                 Zepto Policy Documents
                         │
                         ▼
                     ingest.py
                         │
                         ▼
                      Chunking
                         │
                         ▼
              Sentence Transformer
              all-MiniLM-L6-v2
                         │
                         ▼
                     ChromaDB
                         │
                         ▼
                    User Query
                         │
                         ▼
                   FastAPI /ask
                         │
                         ▼
                    LangGraph
                         │
                  classify_intent
                    /         \
                   /           \
                  ▼             ▼
       Policy Question     General Question
                  │             │
                  ▼             ▼
       retrieve_and_answer   direct_answer
                  │
                  ▼
             Top-3 Retrieval
                  │
                  ▼
           Validated Response
Knowledge Base

The Support Assistant uses eight policy documents:

doc_01_delivery.txt
doc_02_returns_refunds.txt
doc_03_membership.txt
doc_04_tracking.txt
doc_05_cancellation.txt
doc_06_damaged_missing.txt
doc_07_gift_cards.txt
doc_08_support.txt

The documents cover:

Delivery
Returns and refunds
Membership
Tracking
Cancellation
Damaged or missing items
Gift cards
Customer support
Document Ingestion

The ingest.py script:

Loads the policy documents
Splits the documents into chunks
Generates embeddings
Stores the embeddings and chunks in ChromaDB

Embedding model:

all-MiniLM-L6-v2

Run ingestion:

python ingest.py
LangGraph Workflow

The Support Assistant uses a LangGraph StateGraph with three main nodes:

classify_intent
       │
       ├── Policy Question ──► retrieve_and_answer
       │
       └── General Question ─► direct_answer
classify_intent

Classifies the user's query as a policy-related question or a general question.

retrieve_and_answer

For policy-related questions:

Converts the query into an embedding
Searches ChromaDB
Retrieves the top 3 relevant chunks
Generates an answer using the retrieved context
Returns source information and confidence
direct_answer

Handles general questions using the deterministic response configured for mock mode.

Prompt Engineering

The Support Assistant prompt contains:

Role
Context
Task
Format
Length constraint
Negative constraint
Few-shot example

The negative constraint helps prevent the system from inventing unsupported Zepto policies or information.

Response Validation

The response is validated using Pydantic.

Response format:

{
  "answer": "string",
  "sources": [],
  "confidence": 0.0
}

The confidence value is restricted between 0.0 and 1.0.

Mock LLM

The Support Assistant supports:

MOCK_LLM=1

Mock mode is the default configuration.

It allows the application to run without requiring a paid external LLM service.

FastAPI

The application provides:

POST /ask
Example Request
{
  "query": "How much does Zepto Pass cost?"
}
Example Response
{
  "answer": "Based on the retrieved context: ...",
  "sources": [
    "doc_03_membership.txt"
  ],
  "confidence": 1.0
}
General Question Example
{
  "query": "What is Python?"
}

The application returns the configured deterministic response for a non-policy question in mock mode.

Running Support Assistant Locally

Open the terminal in:

support_assistant/

Run:

uvicorn main:app --host 0.0.0.0 --port 7860

Open Swagger UI:

http://localhost:7860/docs
Running with Docker

Open the terminal in:

support_assistant/

Build the Docker image:

docker build -t zepto-support .

Run the container:

docker run --name zepto-support-app -p 8000:7860 zepto-support

The application will be available at:

http://localhost:8000

Swagger UI:

http://localhost:8000/docs
Technologies Used
Data Pipeline
Python
Pandas
Requests
BeautifulSoup
SQLite
SQL
Analytics & Machine Learning
Python
Pandas
NumPy
Matplotlib
Seaborn
Scikit-learn
Imbalanced-learn
Joblib
Support Assistant
Python
Sentence Transformers
ChromaDB
LangGraph
Pydantic
FastAPI
Uvicorn
Docker
Design Decisions
Data Pipeline

Requests and BeautifulSoup are used for web scraping and HTML parsing.

SQLite is used as a lightweight relational database for structured storage and SQL analysis.

Analytics

The Analytics module combines EDA, visualization, preprocessing, classification, class imbalance handling, hyperparameter tuning, and regression.

Support Assistant

The Support Assistant uses local document embeddings and ChromaDB for semantic retrieval.

LangGraph is used to manage the intent classification, retrieval, and direct-answer workflow.

Mock mode is used as the default configuration so the baseline application can run without a paid external LLM service.

Complete Project Workflow
Data Pipeline
cd data_pipeline
python scraper.py
python clean_data.py

Then run the database and query scripts:

python database.py
python pandas_queries.py
Analytics

Navigate to:

cd analytics

Run:

python EDA_analysis.py
python model_traning.py
Support Assistant

Navigate to:

cd support_assistant

Run ingestion:

python ingest.py

Start the API:

uvicorn main:app --host 0.0.0.0 --port 7860

Or run using Docker:

docker build -t zepto-support .
docker run --name zepto-support-app -p 8000:7860 zepto-support
Repository Summary
capstone_project/
│
├── README.md
│
├── data_pipeline/
│   ├── Data Collection
│   ├── Data Cleaning
│   ├── SQLite Database
│   └── SQL Analysis
│
├── analytics/
│   ├── EDA
│   ├── Data Visualization
│   ├── Classification
│   ├── Regression
│   └── Machine Learning Pipeline
│
└── support_assistant/
    ├── Policy Documents
    ├── Document Ingestion
    ├── Embeddings
    ├── ChromaDB
    ├── LangGraph
    ├── FastAPI
    └── Docker
Author

J. Surendra

PGDM Student | Data Analytics | Machine Learning | Artificial Intelligence

GitHub: https://github.com/surendraj2004