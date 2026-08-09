from flask import Flask, request, jsonify
from flask_cors import CORS

from prediction import (
    predict_random_forest,
    predict_decision_tree,
    predict_naive_bayes,
    compare_models
)

from history import (
    create_database,
    save_prediction,
    get_history,
    delete_prediction,
    clear_history
)

from analysis import (
    get_statistics,
    get_model_statistics,
    get_daily_statistics
)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

CORS(app)

create_database()


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "message": "Diabetes Prediction API is running",
        "version": "2.0"
    })


# ============================================================
# PREDICT USING ALL THREE MODELS
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No input data provided"
            }), 400

        # Run all three models
        results = compare_models(data)

        # Save final prediction to history
        history_result = {
            "model": "Ensemble - RF + DT + NB",
            "prediction": results["final_prediction"],
            "probability": results["average_probability"],
            "result": results["final_result"]
        }

        prediction_id = save_prediction(
            data,
            history_result
        )

        results["id"] = prediction_id

        return jsonify(results)

    except Exception as error:

        print("Prediction error:", error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


# ============================================================
# RANDOM FOREST ONLY
# ============================================================

@app.route("/predict/random-forest", methods=["POST"])
def random_forest_api():

    try:

        data = request.get_json()

        result = predict_random_forest(data)

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


# ============================================================
# DECISION TREE ONLY
# ============================================================

@app.route("/predict/decision-tree", methods=["POST"])
def decision_tree_api():

    try:

        data = request.get_json()

        result = predict_decision_tree(data)

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


# ============================================================
# NAIVE BAYES ONLY
# ============================================================

@app.route("/predict/naive-bayes", methods=["POST"])
def naive_bayes_api():

    try:

        data = request.get_json()

        result = predict_naive_bayes(data)

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


# ============================================================
# COMPARE ALL MODELS
# ============================================================

@app.route("/predict/compare", methods=["POST"])
def compare():

    try:

        data = request.get_json()

        results = compare_models(data)

        return jsonify(results)

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


# ============================================================
# GET HISTORY
# ============================================================

@app.route("/history", methods=["GET"])
def history():

    try:

        history_data = get_history()

        return jsonify({
            "success": True,
            "history": history_data
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ============================================================
# DELETE ONE HISTORY RECORD
# ============================================================

@app.route(
    "/history/<int:prediction_id>",
    methods=["DELETE"]
)
def delete_history(prediction_id):

    try:

        deleted = delete_prediction(
            prediction_id
        )

        if not deleted:

            return jsonify({
                "success": False,
                "error": "Prediction not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Prediction deleted"
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ============================================================
# CLEAR ALL HISTORY
# ============================================================

@app.route(
    "/history",
    methods=["DELETE"]
)
def delete_all_history():

    try:

        clear_history()

        return jsonify({
            "success": True,
            "message": "Prediction history cleared"
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ============================================================
# OVERALL ANALYSIS
# ============================================================

@app.route(
    "/analysis",
    methods=["GET"]
)
def analysis():

    try:

        statistics = get_statistics()

        return jsonify({
            "success": True,
            "statistics": statistics
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ============================================================
# MODEL ANALYSIS
# ============================================================

@app.route(
    "/analysis/models",
    methods=["GET"]
)
def model_analysis():

    try:

        statistics = get_model_statistics()

        return jsonify({
            "success": True,
            "models": statistics
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ============================================================
# DAILY ANALYSIS
# ============================================================

@app.route(
    "/analysis/daily",
    methods=["GET"]
)
def daily_analysis():

    try:

        statistics = get_daily_statistics()

        return jsonify({
            "success": True,
            "daily": statistics
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    import os

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )