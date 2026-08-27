import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🏠💻 Real Estate Investment Advisor", page_icon="🏠💻", layout="wide")


st.title("🏠💻 Real Estate Investment Advisor")
st.write(
    "A Streamlit app that explores the Indian residential real-estate market and predicts, for a given property, its estimated price 5 years from now and whether it looks like a good investment."
)
st.link_button("View source on GitHub", "https://github.com/mukundnaramesh2605/Real-Estate-Investment-Advisor---Predicting-Property-Profitability-Future-Value", icon="🔗")

st.divider()
st.subheader("Pages")

st.page_link("pages/1_EDA - Distributions.py", label="EDA: Distributions & Outliers", icon="📊")
st.page_link("pages/2_EDA - Correlations.py", label="EDA: Relationships & Correlations", icon="📊")
st.page_link("pages/3_EDA - Categorical Factors.py", label="EDA: Location & Amenities Factors", icon="📊")
st.page_link("pages/4_EDA - Investment Factors.py", label="EDA: Property & Investment Factors", icon="📊")
st.page_link("pages/5_Prediction.py", label="Price & Good Investment Precition", icon="💻")

markdown_val = """ 
## Model selection & performance

Both prediction tasks were benchmarked across several algorithm families in `Models.ipynb`, with every run tracked in MLflow (`mlflow.db`, experiments `real_estate_regression` and `real_estate_classification`). LightGBM led every other model on both tasks *before* any tuning; hyperparameter tuning (grid search over `learning_rate`, `num_leaves`, `max_depth`, `n_estimators`, `subsample`) then gave a further, smaller edge, after which a "lean" LightGBM configuration reproducing the tuned model's performance with simpler tree settings was promoted to production (`artifacts/real_estate_regression_model_v5`, `artifacts/real_estate_classification_model_v5`).

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

**Why LightGBM:** it was the top performer on the primary ranking metric for *both* tasks (R² for regression, F1/ROC-AUC for classification) before any tuning took place — tuning only widened that lead rather than closing a gap with a different algorithm."""
st.markdown(markdown_val,unsafe_allow_html=False)
reg_chart_data = pd.DataFrame({
    "Model": ["Linear Regression", "Random Forest", "Gradient Boosting", "XGBoost", "LightGBM"],
    "R2": [0.9602, 0.9672, 0.9626, 0.9701, 0.9709],
})
reg_chart_data["Highlight"] = reg_chart_data["Model"] == "LightGBM"
reg_fig = px.bar(
    reg_chart_data,
    x="Model",
    y="R2",
    color="Highlight",
    color_discrete_map={True: "#e63946", False: "#c9d1d9"},
)
reg_fig.update_layout(
    yaxis_range=[0.95, 0.975],
    showlegend=False,
    title_text = "Comparison of each regression model performance",
    xaxis_title="Model",
    yaxis_title="R²",
)
reg_fig.update_traces(texttemplate="%{y:.4f}", textposition="outside")
reg_fig.update_traces(hovertemplate="%{x}<br>R²=%{y:.4f}<extra></extra>")

clf_chart_data = pd.DataFrame({
    "Model": ["Decision Tree", "KNN", "Logistic Regression", "Random Forest",
              "Gradient Boosting", "XGBoost", "LightGBM"],
    "F1": [0.393, 0.256, 0.552, 0.503, 0.029, 0.578, 0.581],
})

clf_chart_data["Highlight"] = clf_chart_data["Model"] == "LightGBM"
clf_fig = px.bar(
    clf_chart_data,
    x="Model",
    y="F1",
    color="Highlight",
    color_discrete_map={True: "#e63946", False: "#c9d1d9"},
)
clf_fig.update_layout(
    showlegend=False,
    title_text ="Comparison of each classification model performance",
    xaxis_title="Model",
    yaxis_title="F1 Score",
)
clf_fig.update_traces(
    texttemplate="%{y:.3f}",
    textposition="outside",
    hovertemplate="%{x}<br>F1=%{y:.3f}<extra></extra>",
)
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(reg_fig, use_container_width=True)

with col2:
    st.plotly_chart(clf_fig, use_container_width=True)