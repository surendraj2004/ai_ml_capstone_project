import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier,plot_tree
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import(
    confusion_matrix,
    accuracy_score,
    precision_score,
    f1_score,
    recall_score,
    roc_curve,
    roc_auc_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE

#making folders
os.makedirs("analytics/charts", exist_ok = True)
os.makedirs("analytics/models", exist_ok = True)

#load the cleaned data
print("=" * 30)
print("LOADING AND INSPECTING THE DATA")
print("=" * 30)
df = pd.read_csv("analytics/titanic_cleaned_data.csv")
print(df.head())
print(df.shape)
#removing columns not required
columns_to_drop = [
    "age_standardized",
    "fare_standardized"
]
#classification of data
X = df.drop(columns=columns_to_drop)
y = df["survived"]
print("=" * 30)
print("CLASS BALANCE")
print("=" * 30)
print(y.value_counts())
print("\n class percentage")
print(y.value_counts(normalize = True) * 100)
#train test split
print("=" * 30)
print(" TRAIN TEST SPLIT")
print("=" * 30)
X_train, X_test, y_train,y_test = train_test_split(
    X,
    y,
   test_size = 0.2,
   random_state = 42,
   stratify = y
   )

print("\n trainingrows", len(X_train))
print("\n testing rows", len(X_test))

print("=" * 30)
print(" Features")
print("=" * 30)
numeric_features = [
    "pclass",
    "age",
    "sibsp",
    "parch",
    "fare"
]
print(numeric_features)
categorical_features = [
    "sex",
    "embarked"
]
print(categorical_features)

#preprocessing
print("=" * 30)
print("PREPROCESSING")
print("=" * 30)
numeric_pipeline = Pipeline(
    steps = [
        (
        "imputer",
        SimpleImputer(strategy = "median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)
categorical_pipeline = Pipeline(
    steps = [
        (
            "imputer",
            SimpleImputer(strategy = "most_frequent")
        ),
        (
            "encoder",
        OneHotEncoder(handle_unknown = "ignore")
        )
    ]
)
preprocessor = ColumnTransformer(
    transformers = [
        (
            "numeric",
            numeric_pipeline,
            numeric_features
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features
        )
    ]
)

#classifiers
print("=" * 30)
print("CLASSIFIERS")
print("=" * 30)
logistic_model = Pipeline(
    steps = [
        ("preprocessor",preprocessor),
        (
            "model", 
            LogisticRegression(max_iter= 1000)
        )
    ]
)

tree_model = Pipeline(
    steps = [
        ("preprocessor", preprocessor),
        (
            "model", 
            DecisionTreeClassifier(
                random_state = 42,
                max_depth = 5
            )
        )
    ]
)

forest_model = Pipeline(
    steps = [
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestClassifier(
                n_estimators = 500,
                random_state = 42
            )
        )
    ]
)
#traning models
print("=" * 30)
print("TRAINING MODELS")
print("=" * 30)

logistic_model =logistic_model.fit(X_train,y_train)

tree_model=tree_model.fit(X_train,y_train)

forest_model=forest_model.fit(X_train,y_train)

#model evaluation
print("=" * 30)
print("MODEL EVALUATION")
print("=" * 30)

def model_eval(name,model):
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:,1]
    cm = confusion_matrix(y_test,predictions)
    accuracy = accuracy_score(y_test,predictions)
    precision = precision_score(y_test,predictions)
    recall = recall_score(y_test,predictions)
    f1 = f1_score(y_test,predictions)
    auc = roc_auc_score(y_test,probabilities)

    print("=" * 30)
    print(name)
    print("=" * 30)

  
    print("CONFUSION MATRIX")
    print(cm)

    print(
        "Accuracy", accuracy,
        "Precision", precision,
        "Recall", recall,
        "F1", f1,
        'AUC', auc
    )

    return{
        "model" : name,
        "accuracy" : accuracy,
        "precision" : precision,
        "recall" : recall,
        "f1" : f1,
        "auc" : auc

    }

    #evaulating three models
print("=" * 30)
print("EVAULATING   ALL THREE MODELS")
print("=" * 30)

results = []
results.append(
    model_eval(
        "Logistic Regression",
        logistic_model
    )
)
results.append(
    model_eval(
        "Decision Tress",
        tree_model
    )
)
results.append(
    model_eval(
        "forest model",
        forest_model
    )
)
results_df = pd.DataFrame(results)
print("=" * 30)
print("MODEL COMPARISON")
print("=" * 30)
print(results_df)

# Decision Tree Visulaization
print("=" * 30)
print("DECISION TREE VISUALIZATION")
print("=" * 30)
tree_model_preprocessed= tree_model.named_steps[
    "preprocessor"
]
tree_classifier = tree_model.named_steps[
    "model"
]

feature_names = (
    tree_model_preprocessed
    .get_feature_names_out()
)
plt.figure(figsize=(20,10))
plot_tree(
    tree_classifier,
    feature_names = feature_names,
    class_names = ["NOT SURVIVED", "SURVIVED"],
    filled = True,
    max_depth = 3 
)
plt.title("Decision Tree Classifier")
plt.savefig("analytics/charts/decision_tree.png")
plt.show()
#roc curves
print("=" * 30)
print("ROC CURVES")
print("=" * 30)
plt.figure(figsize=(8,6))
models = {
    "logistic regression" : logistic_model,
    "decision tree" : tree_model,
    "random forests" : forest_model
}

for name,model in models.items():
    probabilities = model.predict_proba(X_test)[:,1]
    fpr,tpr,threshold = roc_curve(y_test,probabilities)
    auc = roc_auc_score(y_test,probabilities)
    plt.plot(
        fpr,
        tpr,
        label = f"{name} AUC={auc:.3f}"
    )
    plt.plot(
        [0,1],
        [0,1],
        linestyle = "--"
    )
    plt.xlabel("false positive rate")
    plt.ylabel("true positive rates")
    plt.title("roc curves")
    plt.legend()
    plt.savefig("analytics/charts/roc_curves.png")
    plt.show()

# imbalance comparison 
    baseline_model = Pipeline(
        steps = [
            ("preprocessor",preprocessor),
            ("model",
            LogisticRegression(max_iter = 1000)
            )
        ]
    )
    baseline_model.fit(X_train,y_train)
    baseline_predictions = baseline_model.predict(X_test)

    balanced_model = Pipeline(
        steps = [
            ("preprocessor",preprocessor),
            ("model", 
            LogisticRegression(max_iter = 1000,class_weight = "balanced")
            )
        ]
    )
balanced_model.fit(X_train,y_train)
balanced_predictions = balanced_model.predict(X_test)
#smote
print("=" * 30)
print("SMOTE")
print("=" * 30)
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)
smote = SMOTE(random_state = 42)
X_train_smote,y_train_smote = smote.fit_resample(X_train_processed,y_train)
smote_model = LogisticRegression(max_iter = 1000)
smote_model.fit(X_train_smote,y_train_smote)
smote_predictions = smote_model.predict(X_test_processed)
#imbalance results
print("=" * 30)
print("IMBALANCE RESULTS")
print("=" * 30)
imbalance_results = []
def add_imbalance_results(
    name,
    actual,
    predicted
):
    imbalance_results.append({
    "method" : name,
    "precision" : precision_score(actual,predicted),
    "recall" : recall_score(actual,predicted),
    "f1_score" : f1_score(actual,predicted)
})
add_imbalance_results(
    "baseline",y_test,baseline_predictions)

add_imbalance_results(
    "class weight balanced",y_test,balanced_predictions)

add_imbalance_results(
    "smote", y_test,smote_predictions)

imbalance_df = pd.DataFrame(imbalance_results)
print(imbalance_df)
#random forest grid search
print("=" * 30)
print(" random forest grid search")
print("=" * 30)
grid_forest = Pipeline(
    steps = [
        ("preprocessor", preprocessor),
        ("model",
        RandomForestClassifier(random_state= 42,oob_score = True))
    ]
)
parameter_grid = {
    "model__n_estimators" : [
        50,
        100
    ],
    "model__max_depth" : [
        None,
        5,
        10
    ],
    "model__max_features" : [
        "sqrt",
        "log2"
    ] 
}
grid_search = GridSearchCV(
    grid_forest,
    parameter_grid,
    cv=5,
    n_jobs = -1
)

grid_search.fit(X_train,y_train)

print("\n best parameters")
print(grid_search.best_params_)

best_forest = grid_search.best_estimator_
print(best_forest)
print("\n Best validation score")
print(grid_search.best_score_)

print("=" * 30)
print("BEST OOB SCORE")
print("=" * 30)
best_random_forest = (best_forest.named_steps["model"])
print(best_random_forest.oob_score_)

print("=" * 30)
print("regression Fare")
print("=" * 30)
regression_columns = [
    "pclass",
    "age",
    "sibsp",
    "parch",
    "sex",
    "embarked",
    "survived"
]
regression_df = df[
    regression_columns + ["fare"]
].copy()

X_reg =regression_df[regression_columns]
y_reg = regression_df["fare"]
X_reg_train,X_reg_test,y_reg_train,y_reg_test = train_test_split(
X_reg,
y_reg,
test_size = 0.2,
random_state= 42,
)
reg_numeric_features = [
    "pclass",
    "age",
    "sibsp",
    "parch",
    "survived"
]


reg_categorical_features = [
    "sex",
    "embarked"
]
reg_numerical_pipeline = Pipeline(
    steps= [
        ("imputer",
        SimpleImputer(strategy ="median")
        ),
        ("scaler",
        StandardScaler()
        )
    ]
)
reg_categorical_pipeline = Pipeline(
    steps = [
        ("imputer",
        SimpleImputer(strategy = "most_frequent")
        ),
        ("encoder",
        OneHotEncoder(handle_unknown = "ignore")
        )
    ]
)
reg_preprocessor = ColumnTransformer(
    transformers = [
        ("numeric",
        reg_numerical_pipeline,
        reg_numeric_features
        ),
        ("categorical",
        reg_categorical_pipeline,
        reg_categorical_features
        )
    ]
)
regression_model = Pipeline(
    steps = [
        ("preprocessor",reg_preprocessor),
        ("model", LinearRegression())
    ]
)

regression_model.fit(X_reg_train,y_reg_train)
reg_predictions = regression_model.predict(X_reg_test)
print(reg_predictions)
#regression metrics
print("=" * 30)
print("regression metrics")
print("=" * 30)
mae = mean_absolute_error(y_reg_test,reg_predictions)
rmse = mean_squared_error(y_reg_test,reg_predictions)**0.5
r2 = r2_score(y_reg_test,reg_predictions)
number_of_rows = len(y_reg_test)
number_of_features = X_reg_test.shape[1]
adjusted_r2 = (
    1
    -
    (
        (1 - r2)
        *
        (number_of_rows - 1)
        /
        (number_of_rows - number_of_features - 1)
    )
)
print("\nMAE:", mae)

print("RMSE:", rmse)

print("R2:", r2)

print("Adjusted R2:", adjusted_r2)
#residual plot
print("=" * 30)
print("residuals")
print("=" * 30)
residuals = y_reg_test-reg_predictions
plt.figure(figsize=(8, 5))

plt.scatter(
    reg_predictions,
    residuals
)

plt.axhline(
    y=0,
    linestyle="--"
)

plt.xlabel("Predicted Fare")

plt.ylabel("Residual")

plt.title("Regression Residual Plot")

plt.savefig(
    "analytics/charts/residual_plot.png"
)
plt.show()
#final model comparison
print("=" * 30)
print("FINAL MMODEL COMPARISON")
print("=" * 30)
final_comparison = results_df.copy()
print("=" * 30)
print("classification metrics")
print("=" * 30)
print(
    final_comparison[
        [
            "model",
            "accuracy",
            "precision",
            "recall",
            "f1",
            "auc"
        ]
    ]
)
print("=" * 30)
print("regression metrics")
print("=" * 30)
regression_results = pd.DataFrame({
    "MAE": [mae],
    "RMSE": [rmse],
    "R2": [r2],
    "Adjusted_R2": [adjusted_r2]
})
print(regression_results)
#best classifier
print("="*30)
print("BEST CLASSIFIER")
print("="*30)
best_model_name = results_df.loc[
    results_df["f1"].idxmax(),
    "model"
]
print("\nBest classifier based on F1:")

print(best_model_name)
print("="*30)
print("SAVING COMPLETE PIPELINE")
if best_model_name == "Logistic Regression":
    full_pipeline = logistic_model
elif best_model_name == "Decision Tree":
    full_pipeline = tree_model
else:
    full_pipeline = forest_model


joblib.dump(full_pipeline,
"analytics/titanic_pipeline.joblib")
print("\n complete pipeline saved")

##reload saved pipeline
reloaded_pipeline = joblib.load("analytics/titanic_pipeline.joblib")
new_predictions = reloaded_pipeline.predict(X_test.head(5))
print("\n prediction from reloaded pipeline")
print(new_predictions)










    
    

    