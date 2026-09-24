# Module 2 - Analytics

## Overview

This module focuses on Exploratory Data Analysis (EDA), data preprocessing, classification, regression, model evaluation, and saving the final machine learning pipeline using the Titanic dataset.

## Dataset

The Titanic dataset is loaded using:

```python
sns.load_dataset("titanic")

After loading, the dataset is saved locally as:

analytics/titanic.csv

All further analysis and modeling uses the saved dataset.

Files
analytics/
├── README.md
├── titanic.csv
├── titanic_cleaned_data.csv
├── EDA_analysis.py
├── model_training.py
├── titanic_pipeline.joblib
├── models/
└── outputs/
README.md - Module documentation
titanic.csv - Original Titanic dataset
titanic_cleaned_data.csv - Cleaned dataset
EDA_analysis.py - EDA and preprocessing
model_training.py - Classification and regression models
titanic_pipeline.joblib - Saved machine learning pipeline
models/ - Model files
outputs/ - Charts and analysis outputs
1. Exploratory Data Analysis

The dataset is analyzed using:

Shape
Data types
Dataset information
Descriptive statistics
Missing values
Missing-value percentages

Age and Fare are analyzed using histograms and box plots.

Fare is analyzed using:

Mean
Median
Mode
Skewness
2. Missing Value Handling

Missing values are handled based on their percentage:

Less than 5% → drop rows
5% to 30% → impute values
High missing values → drop or encode missing values with justification
3. Outlier Analysis

Outliers are analyzed using the IQR method.

Box plots are used to visualize outliers, especially for Age and Fare.

4. Survival Analysis

Survival is analyzed based on:

Sex
Passenger class
Sex and passenger class

Boolean masking is used for the analysis.

5. Correlation Analysis

The correlation matrix contains exactly these columns:

survived
pclass
age
sibsp
parch
fare

adult_male and alone are excluded.

A heatmap is created to identify relationships between numerical variables. The two strongest absolute off-diagonal correlations are also interpreted.

6. Multivariate Analysis

Multiple multivariate charts are created to analyze relationships between:

Survival
Sex
Passenger class
Age
Fare

Each chart includes a short interpretation.

7. Feature Standardization

Age and Fare are standardized using StandardScaler.

The mean and standard deviation are compared before and after standardization.

8. Classification

The target variable is:

survived

Three classification models are used:

Logistic Regression
Decision Tree
Random Forest

A stratified train-test split is used.

The preprocessing pipeline includes:

Missing-value imputation
Categorical encoding
Numerical scaling

ColumnTransformer and Pipeline are used so that preprocessing is fitted only on the training data.

9. Classification Evaluation

The models are evaluated using:

Confusion Matrix
Accuracy
Precision
Recall
F1 Score
ROC-AUC
10. Class Imbalance

Different approaches are compared:

Baseline model
class_weight="balanced"
SMOTE

SMOTE is applied only to the training data.

11. Random Forest Tuning

GridSearchCV is used to tune the Random Forest model.

The following parameters are tested:

n_estimators
max_depth
max_features

The best parameters and OOB score are reported.

12. Regression

A regression model is used to predict:

fare

The other available features are used as predictors.

The regression model is evaluated using:

MAE
RMSE
R²
Adjusted R²

A residual plot is created and checked for heteroscedasticity.

13. Model Comparison

Classification models are compared using classification metrics.

The regression model is evaluated separately using regression metrics.

A final comparison table and short written recommendation are provided based on the observed results.

14. Model Saving

The complete fitted pipeline is saved using Joblib:

titanic_pipeline.joblib

The saved pipeline is reloaded and tested with raw input data to confirm that it can generate predictions.

15. How to Run

From the project root:

python analytics/EDA_analysis.py

Then:

python analytics/model_training.py

Generated charts, tables, and model files are stored in the appropriate outputs/ and models/ folders.

Technologies Used
Python
Pandas
NumPy
Matplotlib
Seaborn
Scikit-learn
Imbalanced-learn
Joblib
Workflow
Titanic Dataset
      ↓
Data Understanding
      ↓
EDA
      ↓
Missing Value Handling
      ↓
Outlier Analysis
      ↓
Correlation Analysis
      ↓
Feature Standardization
      ↓
Train-Test Split
      ↓
Preprocessing
      ↓
Classification
      ↓
Model Evaluation
      ↓
Random Forest Tuning
      ↓
Fare Regression
      ↓
Model Comparison
      ↓
Save Final Pipeline