import sqlite3
from datetime import datetime
import os


DATABASE_PATH = "database/predictions.db"


def get_connection():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregnancies REAL NOT NULL,
            glucose REAL NOT NULL,
            blood_pressure REAL NOT NULL,
            skin_thickness REAL NOT NULL,
            insulin REAL NOT NULL,
            bmi REAL NOT NULL,
            diabetes_pedigree REAL NOT NULL,
            age REAL NOT NULL,
            prediction INTEGER NOT NULL,
            probability REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_prediction(data, prediction, probability):

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
            prediction,
            probability,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["Pregnancies"],
        data["Glucose"],
        data["BloodPressure"],
        data["SkinThickness"],
        data["Insulin"],
        data["BMI"],
        data["DiabetesPedigreeFunction"],
        data["Age"],
        prediction,
        probability,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_predictions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            pregnancies,
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            bmi,
            diabetes_pedigree,
            age,
            prediction,
            probability,
            created_at
        FROM predictions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    columns = [
        "id",
        "pregnancies",
        "glucose",
        "blood_pressure",
        "skin_thickness",
        "insulin",
        "bmi",
        "diabetes_pedigree",
        "age",
        "prediction",
        "probability",
        "created_at"
    ]

    return [
        dict(zip(columns, row))
        for row in rows
    ]


def get_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM predictions"
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction = 1"
    )

    diabetes = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction = 0"
    )

    no_diabetes = cursor.fetchone()[0]

    connection.close()

    return {
        "total": total,
        "diabetes": diabetes,
        "no_diabetes": no_diabetes
    }