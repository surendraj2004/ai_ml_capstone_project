## Overview

This module focuses on Exploratory Data Analysis (EDA), data preprocessing,
classification, regression, model evaluation, and saving the final machine
learning pipeline using the Titanic dataset.

## Dataset

The Titanic dataset is loaded using Seaborn:

```python
sns.load_dataset("titanic")

After loading, a local copy is saved as:

analytics/titanic.csv

All further analysis and modeling uses the locally saved dataset.

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
File Description
README.md - Documentation for the Analytics module
titanic.csv - Local copy of the Titanic dataset
titanic_cleaned_data.csv - Cleaned Titanic dataset
EDA_analysis.py - Exploratory data analysis and preprocessing
model_training.py - Classification and regression models
titanic_pipeline.joblib - Saved machine learning pipeline
models/ - Model files
outputs/ - Charts and analysis outputs
1. Data Understanding

The dataset is analyzed using:

Dataset shape
Data types
info()
describe()
Missing values
Missing-value percentages
2. Missing Value Handling

Missing values are analyzed for all affected columns.

The following approach is used:

Less than 5% missing values → drop rows
5% to 30% missing values → impute values
High missing values → drop or encode missing values with justification
3. Exploratory Data Analysis

Histograms and box plots are created for:

Age
Fare

Fare is analyzed using:

Mean
Median
Mode
Skewness

Outliers are identified using the IQR method.

4. Survival Analysis

Survival is analyzed using:

Sex
Passenger class
Sex and passenger class

Boolean masking is used to analyze survival patterns.

5. Correlation Analysis

The correlation matrix contains exactly these columns:

survived
pclass
age
sibsp
parch
fare

The columns adult_male and alone are excluded.

A correlation heatmap is created to understand relationships between
the numerical variables.

The two strongest absolute off-diagonal correlations are identified
and interpreted.

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

The mean and standard deviation are compared before and after
standardization.

8. Classification

The target variable is:

survived

Three classification algorithms are used:

Logistic Regression
Decision Tree
Random Forest

A stratified train-test split is used.

The preprocessing pipeline includes:

Missing-value imputation
Categorical encoding
Numerical scaling

ColumnTransformer and Pipeline are used for preprocessing and
model training.

9. Classification Evaluation

The classification models are evaluated using:

Confusion Matrix
Accuracy
Precision
Recall
F1 Score
ROC-AUC
10. Class Imbalance

Class imbalance is analyzed using:

Baseline model
class_weight="balanced"
SMOTE

SMOTE is applied only to the training data.

The results are compared using classification metrics.

11. Random Forest Hyperparameter Tuning

GridSearchCV is used to tune the Random Forest model.

The following parameters are tested:

n_estimators
max_depth
max_features

The best parameters are reported.

The Random Forest OOB score is also reported using:

oob_score=True
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

The classification models are compared using classification metrics.

The regression model is evaluated separately using regression metrics.

A final comparison table is created and a short written recommendation
is provided based on the observed results.

14. Model Saving

The complete fitted machine learning pipeline is saved using Joblib:

titanic_pipeline.joblib

The saved pipeline is reloaded and tested with raw input data to confirm
that it can generate predictions.

15. How to Run

From the project root, run:

python analytics/EDA_analysis.py

Then run:

python analytics/model_training.py

The generated charts, tables, and model files are stored in the
outputs/ and models/ folders.

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
Exploratory Data Analysis
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
Classification Models
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