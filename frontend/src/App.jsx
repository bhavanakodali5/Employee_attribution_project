import Papa from 'papaparse';
import  { useState } from 'react';
import "./App.css";

function App() {
  const [employees, setEmployees] = useState([]);
const [csvError, setCsvError] = useState('');
  const handleCsvUpload = (event) => {
  const file = event.target.files?.[0];

  if (!file) return;
setFile(file);
  setCsvError('');

  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,

    complete: (results) => {
      if (results.errors.length > 0) {
        setCsvError('There was a problem reading the CSV file.');
        return;
      }

      if (!results.meta.fields || results.data.length === 0) {
        setCsvError('The CSV file is empty or has no headers.');
        return;
      }

      setEmployees(results.data);
    },

    error: (error) => {
      setCsvError(error.message);
    },
  });
};

const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

 

  // --------------------------------------------------
  // UPLOAD CSV
  // --------------------------------------------------

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Server error");
      }

      setResult(data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // RENDER
  // --------------------------------------------------

 return ( 
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div className="project-label">MACHINE LEARNING PROJECT</div>

        <h1>Employee Attrition Prediction</h1>

        <p>
          Upload your employee CSV dataset to analyze workforce attrition
          and compare machine learning models.
        </p>
      </header>

      {/* UPLOAD SECTION */}
      <section className="upload-card">

        <div className="upload-icon">
          📊
        </div>

        <h2>Upload Employee Dataset</h2>

        <p className="upload-description">
          Drop your CSV file here or choose a file from your computer.
        </p>

        <label className="file-button">
          Choose CSV File
          <input
         type="file"
         accept=".csv"
         onChange={handleCsvUpload}
/>
        </label>
{csvError && (
  <p role="alert" style={{ color: "red" }}>
    {csvError}
  </p>
)}

{employees.length > 0 && (
  <p>
    Successfully loaded {employees.length} employee records.
  </p>
)}

        {file && (
          <div className="selected-file">
            ✓ Selected file: <strong>{file.name}</strong>
          </div>
        )}

        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={!file || loading}
        >
          {loading ? "Analyzing..." : "Upload & Analyze"}
        </button>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <span>
              Processing dataset and training models...
            </span>
          </div>
        )}

        {error && (
          <div className="error-message">
            ⚠ {error}
          </div>
        )}

      </section>


      {/* RESULTS */}
      {result && (
        <section className="results">

          <div className="results-header">
            <div>
              <div className="section-label">
                ANALYSIS COMPLETE
              </div>

              <h2>Dataset Analysis</h2>

              <p>
                Your employee dataset has been successfully processed.
              </p>
            </div>

            <div className="success-badge">
              ✓ Analysis Complete
            </div>
          </div>


          {/* DATASET INFORMATION */}
          <div className="section-card">

            <h3>Dataset Information</h3>

            <div className="stats-grid">

              <div className="stat-card">
                <span className="stat-label">FILE</span>
                <strong>{result.dataset?.filename}</strong>
              </div>

              <div className="stat-card">
                <span className="stat-label">ROWS</span>
                <strong>{result.dataset?.rows}</strong>
              </div>

              <div className="stat-card">
                <span className="stat-label">COLUMNS</span>
                <strong>{result.dataset?.columns}</strong>
              </div>

              <div className="stat-card">
                <span className="stat-label">TARGET</span>
                <strong>{result.target_column}</strong>
              </div>

            </div>

          </div>


          {/* TARGET DISTRIBUTION */}
          <div className="section-card">

            <h3>Attrition Distribution</h3>

            <p className="section-description">
              Distribution of employees according to the target variable.
            </p>

            <div className="distribution-grid">

              {result.target_distribution &&
                Object.entries(result.target_distribution).map(
                  ([label, count]) => {

                    const total =
                      Object.values(result.target_distribution)
                        .reduce((a, b) => a + b, 0);

                    const percentage =
                      ((count / total) * 100).toFixed(1);

                    return (
                      <div
                        className="distribution-card"
                        key={label}
                      >

                        <div className="distribution-top">
                          <span>{label}</span>
                          <strong>{count}</strong>
                        </div>

                        <div className="progress-bar">
                          <div
                            className="progress-fill"
                            style={{
                              width: `${percentage}%`,
                            }}
                          ></div>
                        </div>

                        <small>
                          {percentage}% of employees
                        </small>

                      </div>
                    );
                  }
                )}

            </div>

          </div>


          {/* DATASET COLUMNS */}
          <div className="section-card">

            <h3>Dataset Columns</h3>

            <p className="section-description">
              Features detected in the uploaded dataset.
            </p>

            <div className="column-list">

              {result.dataset?.column_names?.map(
                (column) => (
                  <span
                    className={
                      column === result.target_column
                        ? "column-tag target"
                        : "column-tag"
                    }
                    key={column}
                  >
                    {column}
                  </span>
                )
              )}

            </div>

          </div>


          {/* MODEL RESULTS */}
          {result.models && (
            <div className="section-card">

              <div className="model-heading">

                <div>
                  <h3>Machine Learning Model Comparison</h3>

                  <p className="section-description">
                    Performance comparison of the classification models.
                  </p>
                </div>

              </div>


              <div className="model-grid">

                {Object.entries(result.models).map(
                  ([modelName, modelData]) => (

                    <div
                      className="model-card"
                      key={modelName}
                    >

                      <div className="model-icon">
                        ML
                      </div>

                      <h4>{modelName}</h4>

                      {typeof modelData === "object" &&
                      modelData !== null ? (

                        <div className="metrics">

                          {Object.entries(modelData).map(
                            ([metric, value]) => (

                              <div
                                className="metric"
                                key={metric}
                              >

                                <span>
                                  {formatMetricName(metric)}
                                </span>

                                <strong>
                                  {formatMetricValue(value)}
                                </strong>

                              </div>

                            )
                          )}

                        </div>

                      ) : (

                        <div className="single-result">
                          {formatMetricValue(modelData)}
                        </div>

                      )}

                    </div>

                  )
                )}

              </div>

            </div>
          )}

        </section>
      )}

    </div>
  );
}


// --------------------------------------------------
// HELPER FUNCTIONS
// --------------------------------------------------

function formatMetricName(name) {
  return name
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}


function formatMetricValue(value) {
  if (typeof value === "number") {

    if (value <= 1) {
      return `${(value * 100).toFixed(2)}%`;
    }

    return value.toFixed(2);
  }

  return String(value);
}


export default App;