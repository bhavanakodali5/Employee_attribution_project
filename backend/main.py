from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import io

from preprocessing import preprocess_data
from model import train_models


# ==================================================
# CREATE FASTAPI APP
# ==================================================

app = FastAPI(
    title="Employee Attrition Prediction API",
    description="Machine Learning API for employee attrition analysis",
    version="1.0"
)


# ==================================================
# CORS CONFIGURATION
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# HOME / HEALTH CHECK
# ==================================================

@app.get("/")
def home():

    return {
        "message": "Employee Attrition Prediction API is running"
    }


# ==================================================
# UPLOAD CSV
# ==================================================

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    # --------------------------------------------------
    # CHECK FILE TYPE
    # --------------------------------------------------

    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file."
        )

    try:

        # --------------------------------------------------
        # READ UPLOADED FILE
        # --------------------------------------------------

        contents = await file.read()

        # Convert uploaded CSV into Pandas DataFrame
        df = pd.read_csv(io.BytesIO(contents))

        # Check if dataset is empty
        if df.empty:

            raise HTTPException(
                status_code=400,
                detail="The uploaded CSV file is empty."
            )

        # --------------------------------------------------
        # DATASET INFORMATION
        # --------------------------------------------------

        dataset_info = {

            "filename": file.filename,

            "rows": int(df.shape[0]),

            "columns": int(df.shape[1]),

            "column_names": df.columns.tolist()
        }

        # --------------------------------------------------
        # FIND ATTRITION COLUMN
        # --------------------------------------------------

        target_column = None

        for column in df.columns:

            if column.strip().lower() == "attrition":

                target_column = column

                break

        # If Attrition column doesn't exist
        if target_column is None:

            raise HTTPException(
                status_code=400,
                detail="The CSV must contain an 'Attrition' column."
            )

        # --------------------------------------------------
        # TARGET DISTRIBUTION
        # --------------------------------------------------

        target_distribution = (
            df[target_column]
            .value_counts()
            .to_dict()
        )

        # Convert values into JSON-compatible format
        target_distribution = {

            str(key): int(value)

            for key, value in target_distribution.items()
        }

        # --------------------------------------------------
        # PREPROCESS DATA
        # --------------------------------------------------

        # IMPORTANT:
        # preprocess_data returns THREE values

        X, y, preprocessor = preprocess_data(
            df,
            target_column
        )

        # --------------------------------------------------
        # TRAIN MACHINE LEARNING MODELS
        # --------------------------------------------------

        results = train_models(
            X,
            y,
            preprocessor
        )

        # --------------------------------------------------
        # SEND RESULT TO FRONTEND
        # --------------------------------------------------

        return {

            "success": True,

            "dataset": dataset_info,

            "target_column": target_column,

            "target_distribution": target_distribution,

            "models": results
        }

    # --------------------------------------------------
    # HANDLE HTTP ERRORS
    # --------------------------------------------------

    except HTTPException:

        raise

    # --------------------------------------------------
    # HANDLE OTHER ERRORS
    # --------------------------------------------------

    except Exception as e:

        print("ERROR:", str(e))

        raise HTTPException(

            status_code=500,

            detail=f"Error processing CSV: {str(e)}"
        )