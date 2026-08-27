import os
import joblib
import streamlit as st

BASE = os.path.dirname(os.path.dirname(__file__))  # ← adjust dirname count to your layout

def _path(*parts):
    return os.path.join(BASE, "artifacts", *parts)

@st.cache_resource
def load_artifacts():
    reg_model  = joblib.load(_path("pkls", "real_estate_regression_model.pkl"))
    clf_model  = joblib.load(_path("pkls", "real_estate_classification_model.pkl"))
    x_reg_cols = joblib.load(_path("x_reg_cols.pkl"))
    x_clf_cols = joblib.load(_path("x_clf_cols.pkl"))
    return reg_model, clf_model, x_reg_cols, x_clf_cols

import pandas as pd

def encode(raw, x_reg_cols, x_clf_cols):
    d = dict(raw)
    d["Public_Transport_Accessibility"] = {"Low":0, "Medium":1, "High":2}[d["Public_Transport_Accessibility"]]
    d["Security"] = {"No":0, "Yes":1}[d["Security"]]

    row = pd.DataFrame([d])
    row["City"] = row["City"].str.replace(" ", "_")
    row["Property_Type"] = row["Property_Type"].str.replace(" ", "_")
    row = pd.get_dummies(row, columns=["City", "Property_Type"], dtype=int)

    reg_row = row.reindex(columns=x_reg_cols, fill_value=0)
    clf_row = row.reindex(columns=x_clf_cols, fill_value=0)
    return reg_row, clf_row

import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def explain_prediction(clf_model, clf_row, top_n=8):
    """
    Returns a DataFrame of the top_n features driving THIS prediction,
    with signed SHAP values (positive = pushes toward 'Good Investment').
    Handles LightGBM classifier SHAP output across versions.
    """
    # pull scaler + model out of the pipeline
    scaler = clf_model.named_steps["scaler"]
    model  = clf_model.named_steps["model"]

    # scale the row exactly as the model saw training data
    scaled = scaler.transform(clf_row)

    # TreeExplainer is exact + fast for LightGBM
    explainer = shap.TreeExplainer(model)
    raw = explainer.shap_values(scaled)

    # normalise to a 1D array of per-feature contributions for class 1
    arr = np.array(raw)
    if arr.ndim == 3:
        vals = arr[0, :, 1]
    elif isinstance(raw, list):
        vals = np.array(raw[1])[0]
    else:
        vals = arr[0]

    contrib = pd.DataFrame({          # ← dedented, aligns with if/elif/else
        "feature": clf_row.columns,
        "shap": vals,
        "value": clf_row.iloc[0].values,
    })

    # 1. drop one-hot columns that are 0 for THIS property
    dummy_prefixes = ("City_", "Property_Type_", "Facing_", "Furnished_Status_", "Owner_Type_")
    is_inactive_dummy = (
        contrib["feature"].str.startswith(dummy_prefixes) & (contrib["value"] == 0)
    )
    contrib = contrib[~is_inactive_dummy]

    # 2. rank by impact, keep top_n
    contrib["abs"] = contrib["shap"].abs()
    contrib = contrib.sort_values("abs", ascending=False).head(top_n)

    return contrib.sort_values("shap")


def plot_explanation(contrib):
    """Horizontal bar: green pushes toward Good, red toward Not-Good."""
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#2ecc71" if v > 0 else "#e74c3c" for v in contrib["shap"]]
    ax.barh(contrib["feature"], contrib["shap"], color=colors)
    ax.axvline(0, color="#888", linewidth=0.8)
    ax.set_xlabel("Impact on 'Good Investment' probability")
    ax.set_title("Why this verdict? (top drivers)")
    plt.tight_layout()
    return fig

def explain_in_words(contrib, good_prob):
    verdict = "a good investment" if good_prob >= 0.5 else "not a good investment"

    # split into supporting (positive) and opposing (negative)
    pos = contrib[contrib["shap"] > 0].sort_values("shap", ascending=False)
    neg = contrib[contrib["shap"] < 0].sort_values("shap")

    def nice(name):
        # make feature names human-readable
        return (name.replace("City_", "being in ")
                    .replace("Property_Type_", "being a ")
                    .replace("_", " "))

    parts = []
    if len(pos):
        top_pos = ", ".join(nice(f) for f in pos["feature"].head(2))
        parts.append(f"**{top_pos}** support{'s' if len(pos)==1 else ''} the verdict")
    if len(neg):
        top_neg = ", ".join(nice(f) for f in neg["feature"].head(2))
        parts.append(f"**{top_neg}** work{'s' if len(neg)==1 else ''} against it")

    reason = "; ".join(parts)
    return f"This property is predicted to be **{verdict}**. {reason}."