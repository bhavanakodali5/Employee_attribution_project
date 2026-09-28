import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def preprocess_data(df, target_column):

    # Make a copy so the original dataframe is not modified
    data = df.copy()

    # --------------------------------------------------
    # CLEAN TARGET
    # --------------------------------------------------

    data[target_column] = (
        data[target_column]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Convert Attrition values:
    # Yes -> 1
    # No  -> 0

    target_mapping = {
        "yes": 1,
        "no": 0,
        "1": 1,
        "0": 0
    }

    data[target_column] = data[target_column].map(target_mapping)

    # Remove rows where target could not be converted
    data = data.dropna(subset=[target_column])

    # --------------------------------------------------
    # SEPARATE FEATURES AND TARGET
    # --------------------------------------------------

    X = data.drop(columns=[target_column])
    y = data[target_column].astype(int)

    # --------------------------------------------------
    # REMOVE CONSTANT / ID-LIKE COLUMNS
    # --------------------------------------------------

    columns_to_remove = []

    for column in X.columns:

        # Remove columns having only one unique value
        if X[column].nunique() <= 1:
            columns_to_remove.append(column)

    # Common ID / unnecessary columns in IBM HR dataset
    unnecessary_columns = [
        "EmployeeNumber",
        "EmployeeCount",
        "Over18",
        "StandardHours"
    ]

    for column in unnecessary_columns:
        if column in X.columns:
            columns_to_remove.append(column)

    columns_to_remove = list(set(columns_to_remove))

    if columns_to_remove:
        X = X.drop(columns=columns_to_remove)

    # --------------------------------------------------
    # IDENTIFY DATA TYPES
    # --------------------------------------------------

    numerical_columns = X.select_dtypes(
        include=["int64", "int32", "float64", "float32"]
    ).columns.tolist()

    categorical_columns = X.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    # --------------------------------------------------
    # PREPROCESSING PIPELINE
    # --------------------------------------------------

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numerical",
                StandardScaler(),
                numerical_columns
            ),
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_columns
            )
        ]
    )

    return X, y, preprocessor