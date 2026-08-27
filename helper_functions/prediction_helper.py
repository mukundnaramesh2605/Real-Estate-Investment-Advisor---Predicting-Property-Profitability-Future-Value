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
    row = pd.get_dummies(row, columns=["City", "Property_Type"], dtype=int)

    reg_row = row.reindex(columns=x_reg_cols, fill_value=0)
    clf_row = row.reindex(columns=x_clf_cols, fill_value=0)
    return reg_row, clf_row