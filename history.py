import sqlite3
import os
from datetime import datetime


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "predictions.db"
)

os.makedirs(DATABASE_DIR, exist_ok=True)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return sqlite3.connect(DATABASE_PATH)


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            pregnancies REAL,
            glucose REAL,
            blood_pressure REAL,
            skin_thickness REAL,
            insulin REAL,
            bmi REAL,
            diabetes_pedigree REAL,
            age REAL,

            model TEXT,
            prediction INTEGER,
            probability REAL,
            result TEXT,

            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()

    return True


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_database():
    return create_database()


# ============================================================
# SAVE PREDICTION
# ============================================================

def save_prediction(data, prediction_result):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            pregnancies,
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            bmi,
            diabetes_pedigree,
            age,
            model,
            prediction,
            probability,
            result,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        data.get("Pregnancies"),
        data.get("Glucose"),
        data.get("BloodPressure"),
        data.get("SkinThickness"),
        data.get("Insulin"),
        data.get("BMI"),
        data.get("DiabetesPedigreeFunction"),
        data.get("Age"),

        prediction_result.get("model"),
        prediction_result.get("prediction"),
        prediction_result.get("probability"),
        prediction_result.get("result"),

        datetime.now().isoformat()
    ))

    prediction_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return prediction_id


# ============================================================
# GET HISTORY
# ============================================================

def get_history():

    connection = get_connection()

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    history = [
        dict(row)
        for row in rows
    ]

    connection.close()

    return history


# ============================================================
# GET SINGLE PREDICTION
# ============================================================

def get_prediction(prediction_id):

    connection = get_connection()

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        WHERE id = ?
    """, (prediction_id,))

    row = cursor.fetchone()

    connection.close()

    if row:
        return dict(row)

    return None


# ============================================================
# DELETE ALL HISTORY
# ============================================================

def clear_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM predictions"
    )

    connection.commit()
    connection.close()

    return True
def delete_prediction(prediction_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM predictions
        WHERE id = ?
        """,
        (prediction_id,)
    )

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted
#loading modules
# ============================================================
# CREATE DATABASE WHEN MODULE LOADS
# ============================================================

create_database()
