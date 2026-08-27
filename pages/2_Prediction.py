import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Overview", page_icon="🧭", layout="wide")

st.title("🧭 Overview")

summary = run_filtered_query(
    db, filters,
    "COUNT(*) AS n, AVG(price) AS avg_price, AVG(rating) AS avg_rating, SUM(reviews) AS total_reviews",
).iloc[0]

if summary["n"] == 0:
    st.warning("No products match the filters.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", f"{summary['n']:,.0f}", border=True)
col2.metric("Avg Price", f"₹{summary['avg_price']:,.2f}", border=True)
col3.metric("Avg Rating", f"{summary['avg_rating']:.2f}", border=True)
col4.metric("Total Reviews", f"{summary['total_reviews']:,.0f}", border=True)

st.divider()

df = get_filtered_df(db, filters, columns="keyword, platform, price_capped")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Distribution")
    fig = px.histogram(df, x="price_capped", nbins=40, color_discrete_sequence=["#2a78d6"])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Products per Keyword")
    keyword_counts = df["keyword"].value_counts().reset_index()
    keyword_counts.columns = ["keyword", "count"]
    fig = px.bar(keyword_counts, x="keyword", y="count", color_discrete_sequence=["#2a78d6"])
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Platform Share")
platform_counts = df["platform"].value_counts().head(8).reset_index()
platform_counts.columns = ["platform", "count"]
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
fig = px.pie(platform_counts, names="platform", values="count", color_discrete_sequence=PALETTE)
fig.update_traces(textposition="outside", textinfo="percent+label")
st.plotly_chart(fig, use_container_width=True)
st.caption("Showing the top 8 platforms only.")
