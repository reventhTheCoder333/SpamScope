"""Train a spam classifier on archive/spam.csv and save artifacts."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

DATA_PATH = Path(__file__).parent / "archive" / "spam.csv"
ARTIFACT_DIR = Path(__file__).parent / "model"
MODEL_PATH = ARTIFACT_DIR / "spam_model.joblib"


def load_dataset() -> tuple[list[str], list[str]]:
    df = pd.read_csv(DATA_PATH, encoding="latin-1", usecols=["v1", "v2"])
    df = df.dropna(subset=["v1", "v2"])
    df["v2"] = df["v2"].astype(str).str.strip()
    df = df[df["v2"].str.len() > 0]
    return df["v2"].tolist(), df["v1"].tolist()


def train() -> Pipeline:
    texts, labels = load_dataset()

    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    max_features=20_000,
                    ngram_range=(1, 2),
                ),
            ),
            (
                "clf",
                LogisticRegression(max_iter=1000, class_weight="balanced"),
            ),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    pipeline.fit(X_train, y_train)
    accuracy = pipeline.score(X_test, y_test)
    print(f"Test accuracy: {accuracy:.2%}")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    return pipeline


if __name__ == "__main__":
    train()
