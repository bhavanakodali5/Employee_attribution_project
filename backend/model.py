from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


def train_models(X, y, preprocessor):

    # --------------------------------------------------
    # TRAIN / TEST SPLIT
    # --------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # --------------------------------------------------
    # DEFINE MODELS
    # --------------------------------------------------

    models = {

        "Logistic Regression": LogisticRegression(
            max_iter=1000
        ),

        "Decision Tree": DecisionTreeClassifier(
            random_state=42,
            max_depth=8
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
    }

    results = {}

    # --------------------------------------------------
    # TRAIN EACH MODEL
    # --------------------------------------------------

    for model_name, model in models.items():

        pipeline = Pipeline(
            steps=[
                (
                    "preprocessing",
                    preprocessor
                ),
                (
                    "model",
                    model
                )
            ]
        )

        # Train
        pipeline.fit(
            X_train,
            y_train
        )

        # Predict
        y_pred = pipeline.predict(
            X_test
        )

        # --------------------------------------------------
        # EVALUATION
        # --------------------------------------------------

        accuracy = accuracy_score(
            y_test,
            y_pred
        )

        precision = precision_score(
            y_test,
            y_pred,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            y_pred,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            y_pred,
            zero_division=0
        )

        results[model_name] = {
            "accuracy": round(
                float(accuracy) * 100,
                2
            ),
            "precision": round(
                float(precision) * 100,
                2
            ),
            "recall": round(
                float(recall) * 100,
                2
            ),
            "f1_score": round(
                float(f1) * 100,
                2
            )
        }

    return results