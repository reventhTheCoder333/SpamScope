# SpamScope

A web app that classifies text messages as **spam** or **ham** (not spam) and shows the spam probability as a percentage.

The model achieves **98.5% accuracy** on the SMS spam dataset.

## Features

- Paste or type any message and get an instant classification
- Visual probability meter with spam / not-spam label
- REST API for programmatic predictions

## Tech Stack

| Layer | Technology |
|-------|------------|
| Model | `MultinomialNB` (Naive Bayes) |
| Vectorizer | `CountVectorizer` |
| Backend | FastAPI |
| Frontend | HTML, CSS, JavaScript |

## Project Structure

```
SpamScope/
├── app.py                          # FastAPI server and /api/predict endpoint
├── train.py                        # Optional script to retrain a model
├── requirements.txt
├── archive/
│   ├── spam.csv                    # Training dataset
│   └── modelsandvectorizers/
│       ├── modelspam.pkl           # Trained classifier
│       └── vectorizerspam.pkl      # Fitted vectorizer
└── static/
    ├── index.html                  # Web UI
    ├── style.css
    └── app.js
```

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

```bash
git clone https://github.com/reventhTheCoder333/SpamScope.git
cd SpamScope
pip install -r requirements.txt
```

### Run the App

```bash
python -m uvicorn app:app --reload
```

Open **http://127.0.0.1:8000** in your browser, enter a message, and click **Analyze**.

## API Usage

**Endpoint:** `POST /api/predict`

**Request:**

```json
{
  "text": "WINNER!! Call now to claim your free prize"
}
```

**Response:**

```json
{
  "label": "spam",
  "spam_probability": 0.682,
  "ham_probability": 0.318
}
```

**Example with curl:**

```bash
curl -X POST http://127.0.0.1:8000/api/predict \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Hey, are we still meeting for lunch?\"}"
```

## Retraining (Optional)

To train a new model from `archive/spam.csv`:

```bash
python train.py
```

This saves a pipeline to `model/spam_model.joblib`. The running app uses the pre-trained artifacts in `archive/modelsandvectorizers/` by default.

## License

This project is open source. Use and modify it freely.
