
import React, { useState } from "react";
import "./App.css";

// Local development:
// VITE_API_URL=http://127.0.0.1:5000
//
// Production:
// VITE_API_URL=https://your-flask-api.onrender.com
const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

const initialForm = {
  Pregnancies: "",
  Glucose: "",
  BloodPressure: "",
  SkinThickness: "",
  Insulin: "",
  BMI: "",
  DiabetesPedigreeFunction: "",
  Age: "",
};

function App() {
  const [formData, setFormData] = useState(initialForm);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handlePredict = async (event) => {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResults(null);

    try {
      const response = await fetch(`${API_URL}/predict/compare`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          Pregnancies: Number(formData.Pregnancies),
          Glucose: Number(formData.Glucose),
          BloodPressure: Number(formData.BloodPressure),
          SkinThickness: Number(formData.SkinThickness),
          Insulin: Number(formData.Insulin),
          BMI: Number(formData.BMI),
          DiabetesPedigreeFunction: Number(
            formData.DiabetesPedigreeFunction
          ),
          Age: Number(formData.Age),
        }),
      });

      const data = await response.json();

      console.log("ML SERVER RESPONSE:", data);

      if (!response.ok || !data.success) {
        throw new Error(data.error || "Prediction failed");
      }

      setResults(data);
    } catch (err) {
      console.error("Prediction error:", err);

      setError(
        `Unable to connect to the ML server. API: ${API_URL}`
      );
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData(initialForm);
    setResults(null);
    setError("");
  };

  const getModelClass = (prediction) => {
    return prediction === 1 ? "model-danger" : "model-safe";
  };

  const getPredictionText = (prediction) => {
    return prediction === 1 ? "Diabetes" : "No Diabetes";
  };

  return (
    <div>
      {/* HEADER */}
      <header className="header">
        <div className="header-content">
          <div className="brand">
            <div className="brand-icon">✚</div>

            <div>
              <h1>Praneeth's Diabetes Prediction</h1>
              <p>Machine Learning Risk Assessment</p>
            </div>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            ML System
          </div>
        </div>
      </header>

      <main className="container">
        {/* INTRO */}
        <section className="intro">
          <h2>Diabetes Risk Prediction</h2>

          <p>
            Enter the patient's clinical information to compare
            predictions from three machine learning models.
          </p>
        </section>

        {/* INPUT CARD */}
        <section className="card">
          <div className="card-title">
            <div>
              <h3>Patient Information</h3>
              <p>
                Enter all values accurately for the best model
                prediction.
              </p>
            </div>
          </div>

          <form onSubmit={handlePredict}>
            <div className="form-grid">
              <InputField
                label="Pregnancies"
                name="Pregnancies"
                value={formData.Pregnancies}
                onChange={handleChange}
                placeholder="e.g. 2"
                min="0"
                required
              />

              <InputField
                label="Glucose"
                name="Glucose"
                value={formData.Glucose}
                onChange={handleChange}
                placeholder="e.g. 120"
                min="0"
                required
              />

              <InputField
                label="Blood Pressure"
                name="BloodPressure"
                value={formData.BloodPressure}
                onChange={handleChange}
                placeholder="e.g. 70"
                min="0"
                required
              />

              <InputField
                label="Skin Thickness"
                name="SkinThickness"
                value={formData.SkinThickness}
                onChange={handleChange}
                placeholder="e.g. 25"
                min="0"
                required
              />

              <InputField
                label="Insulin"
                name="Insulin"
                value={formData.Insulin}
                onChange={handleChange}
                placeholder="e.g. 100"
                min="0"
                required
              />

              <InputField
                label="BMI"
                name="BMI"
                value={formData.BMI}
                onChange={handleChange}
                placeholder="e.g. 32.5"
                min="0"
                step="0.1"
                required
              />

              <InputField
                label="Diabetes Pedigree Function"
                name="DiabetesPedigreeFunction"
                value={formData.DiabetesPedigreeFunction}
                onChange={handleChange}
                placeholder="e.g. 0.45"
                min="0"
                step="0.01"
                required
              />

              <InputField
                label="Age"
                name="Age"
                value={formData.Age}
                onChange={handleChange}
                placeholder="e.g. 35"
                min="1"
                required
              />
            </div>

            <div className="form-actions">
              <button
                type="button"
                className="reset-button"
                onClick={resetForm}
              >
                Reset
              </button>

              <button
                type="submit"
                className="predict-button"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Comparing Models...
                  </>
                ) : (
                  <>
                    Predict & Compare
                    <span>→</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </section>

        {/* ERROR */}
        {error && (
          <div className="error-box">
            <span>!</span>

            <div>
              <strong>Prediction Error</strong>

              <p>{error}</p>
            </div>
          </div>
        )}

        {/* RESULTS */}
        {results && (
          <section className="results-section">
            {/* FINAL RESULT */}
            <div
              className={`final-result ${
                results.final_prediction === 1
                  ? "high-risk"
                  : "low-risk"
              }`}
            >
              <div className="result-top">
                <div>
                  <span className="result-label">
                    FINAL PREDICTION
                  </span>

                  <h2>
                    {results.final_result === "Diabetes"
                      ? "Diabetes Risk Detected"
                      : "No Diabetes Detected"}
                  </h2>
                </div>

                <div className="result-icon">
                  {results.final_prediction === 1 ? "!" : "✓"}
                </div>
              </div>

              <p className="result-description">
                {results.final_prediction === 1
                  ? "The majority of the three machine learning models identified a diabetes-risk pattern."
                  : "The majority of the three machine learning models did not identify a strong diabetes-risk pattern."}
              </p>

              {/* SUMMARY */}
              <div className="summary-grid">
                <div className="summary-item">
                  <span>Average Confidence</span>

                  <strong>
                    {results.average_probability !== undefined
                      ? `${Number(
                          results.average_probability
                        ).toFixed(2)}%`
                      : "N/A"}
                  </strong>
                </div>

                <div className="summary-item">
                  <span>Final Prediction</span>

                  <strong>
                    {getPredictionText(
                      results.final_prediction
                    )}
                  </strong>
                </div>

                <div className="summary-item">
                  <span>Winning Votes</span>

                  <strong>
                    {results.votes ?? 0} /{" "}
                    {results.total_models ?? 3}
                  </strong>
                </div>
              </div>
            </div>

            {/* MODEL COMPARISON */}
            <div className="comparison-card">
              <div className="comparison-heading">
                <div>
                  <span className="result-label">
                    MACHINE LEARNING ANALYSIS
                  </span>

                  <h2>Model Comparison</h2>

                  <p>
                    Three independent models were evaluated and
                    compared using majority voting.
                  </p>
                </div>

                <div className="models-count">
                  3 Models
                </div>
              </div>

              <div className="models-grid">
                <ModelCard
                  title="Random Forest"
                  icon="🌲"
                  result={results.random_forest}
                  getModelClass={getModelClass}
                  getPredictionText={getPredictionText}
                />

                <ModelCard
                  title="Decision Tree"
                  icon="🌳"
                  result={results.decision_tree}
                  getModelClass={getModelClass}
                  getPredictionText={getPredictionText}
                />

                <ModelCard
                  title="Naive Bayes"
                  icon="🧠"
                  result={results.naive_bayes}
                  getModelClass={getModelClass}
                  getPredictionText={getPredictionText}
                />
              </div>
            </div>

            {/* VOTING */}
            <div className="voting-card">
              <h3>Majority Voting Result</h3>

              <div className="vote-row">
                <div className="vote-option">
                  <span>Diabetes</span>

                  <strong>
                    {results.diabetes_votes ??
                      (results.final_prediction === 1
                        ? results.votes
                        : 0)}
                    votes
                  </strong>
                </div>

                <div className="vote-option">
                  <span>No Diabetes</span>

                  <strong>
                    {results.no_diabetes_votes ??
                      (results.final_prediction === 0
                        ? results.votes
                        : 0)}
                    votes
                  </strong>
                </div>
              </div>

              <div className="voting-explanation">
                Final result is determined by the majority decision
                of Random Forest, Decision Tree, and Naive Bayes.
              </div>
            </div>

            <div className="medical-note">
              <strong>Important:</strong> This application is an
              educational machine-learning demonstration and should
              not be used as a substitute for professional medical
              diagnosis.
            </div>
          </section>
        )}
      </main>

      <footer>
        <p>
          Diabetes Prediction System • Random Forest • Decision Tree •
          Naive Bayes
        </p>
      </footer>
    </div>
  );
}

/* ============================================================
   INPUT COMPONENT
============================================================ */

function InputField({
  label,
  name,
  value,
  onChange,
  placeholder,
  min,
  step,
  required,
}) {
  return (
    <div className="input-group">
      <label htmlFor={name}>{label}</label>

      <input
        id={name}
        name={name}
        type="number"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        min={min}
        step={step}
        required={required}
      />
    </div>
  );
}

/* ============================================================
   MODEL CARD COMPONENT
============================================================ */

function ModelCard({
  title,
  icon,
  result,
  getModelClass,
  getPredictionText,
}) {
  if (!result) {
    return null;
  }

  return (
    <div
      className={`model-card ${getModelClass(
        result.prediction
      )}`}
    >
      <div className="model-card-header">
        <div className="model-icon">{icon}</div>

        <div>
          <h3>{title}</h3>
          <span>Individual Model</span>
        </div>
      </div>

      <div className="model-prediction">
        <span>Prediction</span>

        <strong>
          {getPredictionText(result.prediction)}
        </strong>
      </div>

      <div className="confidence">
        <div className="confidence-header">
          <span>Confidence</span>

          <strong>
            {result.probability !== undefined
              ? `${Number(result.probability).toFixed(2)}%`
              : "N/A"}
          </strong>
        </div>

        <div className="progress">
          <div
            className="progress-bar"
            style={{
              width: `${Math.min(
                Math.max(
                  Number(result.probability) || 0,
                  0
                ),
                100
              )}%`,
            }}
          ></div>
        </div>
      </div>

      <div className="model-status">
        {result.prediction === 1
          ? "Risk pattern detected"
          : "No strong risk pattern"}
      </div>
    </div>
  );
}

export default App;

