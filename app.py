from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ARTIFACT_DIR = Path(__file__).parent / "archive" / "modelsandvectorizers"
VECTORIZER_PATH = ARTIFACT_DIR / "vectorizerspam.pkl"
MODEL_PATH = ARTIFACT_DIR / "modelspam.pkl"
STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Spam Detector")

_vectorizer = None
_model = None


def get_artifacts():
    global _vectorizer, _model
    if _vectorizer is None or _model is None:
        if not VECTORIZER_PATH.exists() or not MODEL_PATH.exists():
            raise HTTPException(
                status_code=503,
                detail="Model artifacts not found in archive/modelsandvectorizers.",
            )
        _vectorizer = joblib.load(VECTORIZER_PATH)
        _model = joblib.load(MODEL_PATH)
    return _vectorizer, _model


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10_000)


class PredictResponse(BaseModel):
    label: str
    spam_probability: float
    ham_probability: float


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/predict", response_model=PredictResponse)
async def predict(body: PredictRequest):
    text = body.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    vectorizer, model = get_artifacts()
    features = vectorizer.transform([text])
    proba = model.predict_proba(features)[0]
    classes = list(model.classes_)

    ham_idx = classes.index("ham")
    spam_idx = classes.index("spam")
    ham_prob = float(proba[ham_idx])
    spam_prob = float(proba[spam_idx])
    label = "spam" if spam_prob >= 0.5 else "ham"

    return PredictResponse(
        label=label,
        spam_probability=round(spam_prob, 4),
        ham_probability=round(ham_prob, 4),
    )


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
