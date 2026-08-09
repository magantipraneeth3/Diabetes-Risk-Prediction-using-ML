import os

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB


# ==================================================
# Paths
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "diabetes.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ==================================================
# Load dataset
# ==================================================

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print(
    f"Dataset loaded: {df.shape}"
)


# ==================================================
# Features and target
# ==================================================

FEATURES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
]

TARGET = "Outcome"


X = df[FEATURES]

y = df[TARGET]


# ==================================================
# Train / Test split
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


# ==================================================
# Scaling
# ==================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)


# ==================================================
# Random Forest
# ==================================================

print("Training Random Forest...")

random_forest = RandomForestClassifier(

    n_estimators=200,

    max_depth=None,

    random_state=42,

    class_weight="balanced"

)

random_forest.fit(
    X_train_scaled,
    y_train
)


# ==================================================
# Decision Tree
# ==================================================

print("Training Decision Tree...")

decision_tree = DecisionTreeClassifier(

    max_depth=6,

    random_state=42,

    class_weight="balanced"

)

decision_tree.fit(
    X_train_scaled,
    y_train
)


# ==================================================
# Naive Bayes
# ==================================================

print("Training Naive Bayes...")

naive_bayes = GaussianNB()

naive_bayes.fit(
    X_train_scaled,
    y_train
)


# ==================================================
# Save models
# ==================================================

joblib.dump(

    random_forest,

    os.path.join(
        MODEL_DIR,
        "randomforest.pkl"
    )
)

joblib.dump(

    decision_tree,

    os.path.join(
        MODEL_DIR,
        "decisiontree.pkl"
    )
)

joblib.dump(

    naive_bayes,

    os.path.join(
        MODEL_DIR,
        "naivebayes.pkl"
    )
)

joblib.dump(

    scaler,

    os.path.join(
        MODEL_DIR,
        "scaler.pkl"
    )
)


print()
print("======================================")
print("MODEL TRAINING COMPLETE")
print("======================================")

print()
print("Created:")

print(
    "models/randomforest.pkl"
)

print(
    "models/decisiontree.pkl"
)

print(
    "models/naivebayes.pkl"
)

print(
    "models/scaler.pkl"
)

print()