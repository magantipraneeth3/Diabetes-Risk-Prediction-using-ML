
import os
import joblib
import numpy as np


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


# ============================================================
# LOAD MODELS
# ============================================================

random_forest = joblib.load(
    os.path.join(MODEL_DIR, "randomforest.pkl")
)

decision_tree = joblib.load(
    os.path.join(MODEL_DIR, "decisiontree.pkl")
)

naive_bayes = joblib.load(
    os.path.join(MODEL_DIR, "naivebayes.pkl")
)

scaler = joblib.load(
    os.path.join(MODEL_DIR, "scaler.pkl")
)


# ============================================================
# FEATURES
# ============================================================

FEATURES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
]


# ============================================================
# PREPARE INPUT
# ============================================================

def prepare_input(data):

    values = []

    for feature in FEATURES:

        if feature not in data:
            raise ValueError(
                f"Missing feature: {feature}"
            )

        try:
            value = float(data[feature])
        except (ValueError, TypeError):
            raise ValueError(
                f"Invalid value for {feature}"
            )

        values.append(value)

    X = np.array(values).reshape(1, -1)

    return scaler.transform(X)


# ============================================================
# GENERIC MODEL PREDICTION
# ============================================================

def run_model(model, model_name, data):

    X = prepare_input(data)

    prediction = int(model.predict(X)[0])

    probabilities = model.predict_proba(X)[0]

    # Find probability of the predicted class
    class_index = list(model.classes_).index(prediction)

    confidence = float(
        probabilities[class_index] * 100
    )

    result = (
        "Diabetes"
        if prediction == 1
        else "No Diabetes"
    )

    return {
        "model": model_name,
        "prediction": prediction,
        "probability": round(confidence, 2),
        "result": result,
        "success": True
    }


# ============================================================
# RANDOM FOREST
# ============================================================

def predict_random_forest(data):

    return run_model(
        random_forest,
        "Random Forest",
        data
    )


# ============================================================
# DECISION TREE
# ============================================================

def predict_decision_tree(data):

    return run_model(
        decision_tree,
        "Decision Tree",
        data
    )


# ============================================================
# NAIVE BAYES
# ============================================================

def predict_naive_bayes(data):

    return run_model(
        naive_bayes,
        "Naive Bayes",
        data
    )


# ============================================================
# COMPARE ALL MODELS
# ============================================================

def compare_models(data):

    rf = predict_random_forest(data)

    dt = predict_decision_tree(data)

    nb = predict_naive_bayes(data)

    predictions = [
        rf["prediction"],
        dt["prediction"],
        nb["prediction"]
    ]

    # Count votes
    diabetes_votes = predictions.count(1)

    no_diabetes_votes = predictions.count(0)

    # Majority voting
    if diabetes_votes > no_diabetes_votes:

        final_prediction = 1
        final_result = "Diabetes"
        winning_votes = diabetes_votes

    else:

        final_prediction = 0
        final_result = "No Diabetes"
        winning_votes = no_diabetes_votes

    # Average model confidence
    average_probability = (
        rf["probability"]
        + dt["probability"]
        + nb["probability"]
    ) / 3

    return {

        "success": True,

        # Individual models
        "random_forest": rf,
        "decision_tree": dt,
        "naive_bayes": nb,

        # Final result
        "final_prediction": final_prediction,
        "final_result": final_result,

        # Voting
        "diabetes_votes": diabetes_votes,
        "no_diabetes_votes": no_diabetes_votes,
        "votes": winning_votes,
        "total_models": 3,

        # Confidence
        "average_probability": round(
            average_probability,
            2
        )
    }

