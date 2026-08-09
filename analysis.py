import sqlite3
import os


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "predictions.db"
)


# ============================================================
# GET DATABASE CONNECTION
# ============================================================

def get_connection():

    return sqlite3.connect(
        DATABASE_PATH
    )


# ============================================================
# GET BASIC STATISTICS
# ============================================================

def get_statistics():

    connection = get_connection()

    cursor = connection.cursor()

    # Total predictions
    cursor.execute(
        "SELECT COUNT(*) FROM predictions"
    )

    total_predictions = cursor.fetchone()[0]

    # Diabetes predictions
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM predictions
        WHERE prediction = 1
        """
    )

    diabetes_predictions = cursor.fetchone()[0]

    # No diabetes predictions
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM predictions
        WHERE prediction = 0
        """
    )

    no_diabetes_predictions = cursor.fetchone()[0]

    # Average probability
    cursor.execute(
        """
        SELECT AVG(probability)
        FROM predictions
        """
    )

    average_probability = cursor.fetchone()[0]

    connection.close()

    if average_probability is None:
        average_probability = 0

    return {
        "total_predictions": total_predictions,
        "diabetes_predictions": diabetes_predictions,
        "no_diabetes_predictions": no_diabetes_predictions,
        "average_probability": round(
            average_probability,
            2
        )
    }


# ============================================================
# MODEL STATISTICS
# ============================================================

def get_model_statistics():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            model,
            COUNT(*) AS total,
            AVG(probability) AS average_probability
        FROM predictions
        GROUP BY model
        """
    )

    rows = cursor.fetchall()

    connection.close()

    result = []

    for row in rows:

        result.append({
            "model": row[0],
            "total": row[1],
            "average_probability": round(
                row[2] if row[2] is not None else 0,
                2
            )
        })

    return result


# ============================================================
# RESULT DISTRIBUTION
# ============================================================

def get_result_distribution():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            result,
            COUNT(*)
        FROM predictions
        GROUP BY result
        """
    )

    rows = cursor.fetchall()

    connection.close()

    distribution = {}

    for result, count in rows:

        distribution[result] = count

    return distribution


# ============================================================
# AGE ANALYSIS
# ============================================================

def get_age_analysis():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            AVG(age),
            MIN(age),
            MAX(age)
        FROM predictions
        """
    )

    row = cursor.fetchone()

    connection.close()

    return {
        "average_age": round(
            row[0] if row[0] is not None else 0,
            2
        ),
        "minimum_age": row[1],
        "maximum_age": row[2]
    }


# ============================================================
# GLUCOSE ANALYSIS
# ============================================================

def get_glucose_analysis():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            AVG(glucose),
            MIN(glucose),
            MAX(glucose)
        FROM predictions
        """
    )

    row = cursor.fetchone()

    connection.close()

    return {
        "average_glucose": round(
            row[0] if row[0] is not None else 0,
            2
        ),
        "minimum_glucose": row[1],
        "maximum_glucose": row[2]
    }


# ============================================================
# BMI ANALYSIS
# ============================================================

def get_bmi_analysis():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            AVG(bmi),
            MIN(bmi),
            MAX(bmi)
        FROM predictions
        """
    )

    row = cursor.fetchone()

    connection.close()

    return {
        "average_bmi": round(
            row[0] if row[0] is not None else 0,
            2
        ),
        "minimum_bmi": row[1],
        "maximum_bmi": row[2]
    }


# ============================================================
# COMPLETE DASHBOARD ANALYSIS
# ============================================================

def get_complete_analysis():

    return {
        "statistics": get_statistics(),
        "model_statistics": get_model_statistics(),
        "result_distribution": get_result_distribution(),
        "age_analysis": get_age_analysis(),
        "glucose_analysis": get_glucose_analysis(),
        "bmi_analysis": get_bmi_analysis()
    }


def get_daily_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            DATE(created_at) AS prediction_date,
            COUNT(*) AS total_predictions,
            SUM(
                CASE
                    WHEN prediction = 1 THEN 1
                    ELSE 0
                END
            ) AS diabetes_predictions,
            SUM(
                CASE
                    WHEN prediction = 0 THEN 1
                    ELSE 0
                END
            ) AS no_diabetes_predictions
        FROM predictions
        GROUP BY DATE(created_at)
        ORDER BY prediction_date ASC
    """)

    rows = cursor.fetchall()

    connection.close()

    daily_statistics = []

    for row in rows:

        daily_statistics.append({
            "date": row[0],
            "total_predictions": row[1],
            "diabetes_predictions": row[2] or 0,
            "no_diabetes_predictions": row[3] or 0
        })

    return daily_statistics