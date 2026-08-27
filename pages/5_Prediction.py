import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
from helper_functions.dataset_reader import dataset_reader
from helper_functions.prediction_helper import load_artifacts,encode
from helper_functions.prediction_helper import explain_prediction, plot_explanation,explain_in_words
st.set_page_config(page_title="Predictions", page_icon="💻", layout="wide")

st.title("💻 Predictions")

reader = dataset_reader()
cities = reader.get_cities()
property_types = reader.get_property_type()

st.title("Property Investment Prediction")

c1, c2, c3 = st.columns(3)
with c1:
    bhk = st.number_input("BHK", 1, 10, 2)
    size = st.number_input("Size (Sq Ft)", 100, 10000, 1000)
    price = st.number_input("Current Price (Lakhs)", 1.0, 1000.0, 50.0)
    floor = st.number_input("Floor No", 0, 100, 3)
    total_floors = st.number_input("Total Floors", 1, 100, 10)
with c2:
    age = st.number_input("Age of Property", 0, 100, 5)
    schools = st.number_input("Nearby Schools", 0, 50, 5)
    hospitals = st.number_input("Nearby Hospitals", 0, 50, 3)
    parking = st.number_input("Parking Spaces", 0, 10, 1)
    amenities = st.number_input("Amenities Count", 0, 20, 5)
with c3:
    city = st.selectbox("City", cities)
    ptype = st.selectbox("Property Type", property_types)
    transport = st.selectbox("Public Transport", ["Low", "Medium", "High"])
    security = st.selectbox("Security", ["No", "Yes"])

if st.button("Predict"):
    raw = {
        "BHK": bhk, "Size_in_SqFt": size, "Price_in_Lakhs": price,
        "Floor_No": floor, "Total_Floors": total_floors, "Age_of_Property": age,
        "Nearby_Schools": schools, "Nearby_Hospitals": hospitals,
        "Parking_Space": parking, "Amenities_Count": amenities,
        "City": city, "Property_Type": ptype,
        "Public_Transport_Accessibility": transport, "Security": security,
    }

    reg_model, clf_model, x_reg_cols, x_clf_cols = load_artifacts()

    reg_row, clf_row = encode(raw, x_reg_cols, x_clf_cols)
    print("shapes:", reg_row.shape, clf_row.shape)          # want (1,57) (1,54)
    print("city set:", reg_row.filter(like="City_").sum(axis=1).values)  # want [1]
    print("BHK in clf?", "BHK" in clf_row.columns)          # want False
    future_price = reg_model.predict(reg_row)[0]
    good_prob = clf_model.predict_proba(clf_row)[0][1]
    verdict = "Good Investment ✅" if good_prob >= 0.5 else "Not a Good Investment ❌"

    st.subheader("Results")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Estimated Price after 5 Years", f"₹{future_price:,.1f} Lakhs")
    with col_b:
        st.write(f"**Investment Verdict:** {verdict}")
        st.caption(f"Model confidence: {good_prob*100:.0f}%  (threshold 50%)")


    st.subheader("Why this verdict?")
    contrib = explain_prediction(clf_model, clf_row)
    st.pyplot(plot_explanation(contrib))
    st.write(explain_in_words(contrib, good_prob))