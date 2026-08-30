# 🏠💻 Real Estate Investment Advisor

A Streamlit app that explores the Indian residential real-estate market and predicts, for a given property, its **estimated price 5 years from now** and whether it looks like a **good investment**.

The app is built on top of a housing-price dataset that has been enriched with engineered target columns (`Future_Price_5Y`, `Good_Investment`), and ships with a regression model and a classification model trained on that data.

**Live source:** https://real-estate-investment-advisor-26.streamlit.app/

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
├── Models.ipynb                   # Model training/evaluation notebook, also logs runs to MLflow
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
- `Models.ipynb` — trains the regression (future price) and classification (good investment) models, exports the artifacts consumed by the Streamlit app, and logs every run's params/metrics/model to MLflow (tracking data stored locally in `mlflow.db`/`mlartifacts/`, ignored by git).

## How the target columns were built

Both prediction targets are engineered in `EDA.ipynb` from the raw listing columns rather than being observed market outcomes — worth knowing before reading the model performance numbers below.

- **`Future_Price_5Y`** — base = `Price_in_Lakhs × (1 + city_growth_rate)^5`, where the annual growth rate is adjusted by property-type and age effects, plus Gaussian noise, before compounding.
- **`Good_Investment`** — a score out of 4, labeled "good" if it hits 3 or more:
  - Price/sqft below the city median
  - BHK ≥ 3
  - Ready_to_Move
  - Parking = Yes AND Amenities_Count ≥ 3

## Model selection & performance

Both prediction tasks were benchmarked across several algorithm families in `Models.ipynb`:

- **Regression** (`Future_Price_5Y`): Linear Regression, Ridge, Lasso, Random Forest, Gradient Boosting, XGBoost, LightGBM.
- **Classification** (`Good_Investment`): Decision Tree, KNN, Logistic Regression, Random Forest, Gradient Boosting, XGBoost, LightGBM.

Every run was tracked in MLflow (`mlflow.db`, experiments `real_estate_regression` and `real_estate_classification`). LightGBM led every other model on both tasks *before* any tuning; hyperparameter tuning (grid search over `learning_rate`, `num_leaves`, `max_depth`, `n_estimators`, `subsample`) then gave a further, smaller edge, after which a "lean" LightGBM configuration reproducing the tuned model's performance with simpler tree settings was promoted to production (`artifacts/real_estate_regression_model_v5`, `artifacts/real_estate_classification_model_v5`).

### Regression — 5-year future price (`Future_Price_5Y`)

| Model | R² ↑ | RMSE ↓ (Lakhs) | MAE ↓ (Lakhs) |
|---|---|---|---|
| Linear Regression | 0.9602 | 39.05 | 29.32 |
| Ridge | 0.9602 | 39.05 | 29.32 |
| Lasso | 0.9591 | 39.57 | 29.08 |
| Random Forest | 0.9672 | 35.43 | 24.71 |
| Gradient Boosting | 0.9626 | 37.87 | 26.61 |
| XGBoost | 0.9701 | 33.82 | 23.47 |
| **LightGBM (baseline)** | 0.9708 | 33.45 | 23.28 |
| LightGBM (tuned) | 0.9709 | 33.37 | 23.22 |
| **LightGBM lean, tuned — deployed (v5)** | 0.9709 | 33.38 | 23.22 |

- Even untuned, LightGBM already beat every other model tried on all three metrics.
- Tuning (`n_estimators=200`, `num_leaves=31`, `learning_rate=0.05`, `subsample=0.7`) trimmed RMSE by another ~0.3% — a small, consistent gain rather than a step change.
- The deployed "lean" configuration matches the fully tuned model's accuracy with a simpler hyperparameter set.

### Classification — good investment (`Good_Investment`)

The target is imbalanced (~27.6% of properties are labeled "Good Investment" — see the *EDA: Investment Factors* page), so accuracy alone is a misleading way to pick a model; ROC-AUC and F1 were used instead.

| Model | ROC-AUC ↑ | F1 ↑ | Precision | Recall | Accuracy |
|---|---|---|---|---|---|
| Decision Tree | 0.579 | 0.393 | 0.386 | 0.401 | 0.659 |
| KNN | 0.576 | 0.256 | 0.365 | 0.197 | 0.684 |
| Logistic Regression | 0.723 | 0.552 | 0.450 | 0.713 | 0.681 |
| Random Forest | 0.722 | 0.503 | 0.445 | 0.579 | 0.685 |
| Gradient Boosting | 0.722 | 0.029 | 0.428 | 0.015 | **0.723** |
| XGBoost | 0.722 | 0.578 | 0.446 | 0.819 | 0.670 |
| **LightGBM (baseline)** | 0.723 | 0.580 | 0.446 | 0.831 | 0.669 |
| LightGBM (tuned) | 0.723 | 0.581 | 0.446 | 0.833 | 0.669 |
| **LightGBM lean, tuned — deployed (v5)** | 0.721 | 0.581 | 0.446 | 0.834 | 0.669 |

- Gradient Boosting shows the highest raw accuracy (72.3%), but that's a red flag rather than a win — its recall is 1.5%, meaning it almost never predicts "Good Investment" and is effectively just guessing the majority class.
- LightGBM has the best F1 and ROC-AUC of every model tried, both before and after tuning, while actually surfacing good-investment properties (~83% recall).
- Tuning (`max_depth=20`, same `learning_rate`/`num_leaves`/`subsample` as baseline) nudged F1 up slightly; the deployed "lean" variant (`num_leaves=70`, `max_depth=-1`, `subsample=0.8`, fewer estimators) reproduces that performance.

**Why LightGBM:** it was the top performer on the primary ranking metric for *both* tasks (R² for regression, F1/ROC-AUC for classification) before any tuning took place — tuning only widened that lead rather than closing a gap with a different algorithm.

## Notes

- The `Datasets/` CSVs are sizeable (tens of MB) since they contain the full housing dataset plus engineered/encoded columns.
- MLflow tracking artifacts (`mlruns/`, `mlartifacts/`, `mlflow.db`) are local-only and excluded from version control via `.gitignore`.
