# 🏠💻 Real Estate Investment Advisor

A Streamlit app that explores the Indian residential real-estate market and predicts, for a given property, its **estimated price 5 years from now** and whether it looks like a **good investment**.

The app is built on top of a housing-price dataset that has been enriched with engineered target columns (`Future_Price_5Y`, `Good_Investment`), and ships with a regression model and a classification model trained on that data.

**Live source:** https://github.com/mukundnaramesh2605/Real-Estate-Investment-Advisor---Predicting-Property-Profitability-Future-Value

## Features

The app is a multi-page Streamlit application:

| Page | Description |
|---|---|
| `Home.py` | Landing page with navigation links to every page. |
| `pages/1_EDA - Distributions.py` | Distributions and outliers for price, size, and other numeric fields. |
| `pages/2_EDA - Correlations.py` | Relationships and correlations between numeric features and the target columns. |
| `pages/3_EDA - Categorical Factors.py` | Breakdown of price and investment quality by location and amenity factors. |
| `pages/4_EDA - Investment Factors.py` | Property and investment factor analysis (furnished status, ownership, parking, amenities, etc.). |
| `pages/5_Prediction.py` | Interactive prediction: enter property details and get a 5-year price estimate plus a "Good Investment" verdict. |

## Project structure

```
.
├── Home.py                        # Streamlit entry point
├── pages/                         # Streamlit multi-page app pages (EDA + Prediction)
├── helper_functions/
│   ├── dataset_reader.py          # Cached dataset loading + dropdown value helpers
│   ├── eda_helpers.py             # Cached aggregation helpers used by the EDA pages
│   └── prediction_helper.py       # Loads model artifacts and encodes user input for inference
├── artifacts/
│   ├── pkls/                      # Trained regression & classification models (joblib)
│   ├── x_reg_cols.pkl             # Column order/schema expected by the regression model
│   ├── x_clf_cols.pkl             # Column order/schema expected by the classification model
│   ├── scaler_reg.pkl / scaler_clf.pkl
│   └── real_estate_*_model_v5/    # MLflow model artifacts (conda.yaml, requirements.txt, etc.)
├── Datasets/                      # Source and processed CSV datasets
├── EDA.ipynb                      # Exploratory data analysis notebook
├── Models.ipynb                   # Model training/evaluation notebook
├── MLflow.ipynb                   # MLflow experiment tracking notebook
└── requirements.txt                # Python dependencies to run the Streamlit app
```

## Getting started

### Prerequisites

- Python 3.11+ (models were trained under Python 3.11)

### Setup

```bash
# clone the repo
git clone https://github.com/mukundnaramesh2605/Real-Estate-Investment-Advisor---Predicting-Property-Profitability-Future-Value.git
cd "Real Estate Investment Advisor - Predicting Property Profitability & Future Value"

# create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run Home.py
```

Streamlit will start a local server (default: http://localhost:8501) and open the app in your browser. Use the sidebar to move between the EDA pages and the Prediction page.

## Using the Prediction page

On the **Prediction** page, fill in the property details (BHK, size, current price, floor, age, nearby amenities, city, property type, transport accessibility, security) and click **Predict** to get:

- **Estimated Price after 5 Years** — output of the regression model.
- **Investment Verdict** — "Good Investment" or "Not a Good Investment" from the classification model, along with the model's confidence.

Predictions rely on the pre-trained artifacts in `artifacts/pkls/` and the column schemas in `artifacts/x_reg_cols.pkl` / `artifacts/x_clf_cols.pkl`, which must stay in sync with any retraining done in `Models.ipynb`.

## Data & modeling notebooks

- `EDA.ipynb` — initial data exploration and feature engineering used to build the enriched datasets in `Datasets/`.
- `Models.ipynb` — trains the regression (future price) and classification (good investment) models and exports the artifacts consumed by the Streamlit app.
- `MLflow.ipynb` — logs experiments, metrics, and model versions to MLflow (tracking data stored locally, ignored by git).

## Notes

- The `Datasets/` CSVs are sizeable (tens of MB) since they contain the full housing dataset plus engineered/encoded columns.
- MLflow tracking artifacts (`mlruns/`, `mlartifacts/`, `mlflow.db`) are local-only and excluded from version control via `.gitignore`.
