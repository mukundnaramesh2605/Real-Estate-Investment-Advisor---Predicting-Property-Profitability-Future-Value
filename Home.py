import streamlit as st

st.set_page_config(page_title="🏠💻 Real Estate Investment Advisor", page_icon="🏠💻", layout="wide")


st.title("🏠💻 Real Estate Investment Advisor")
st.write(
    "This app looks at product listings scraped from different shopping sites "
    "(price, rating, reviews, search ranking) to see which brands and platforms "
    "show up the most. Use the sidebar to filter the data, it updates all the pages."
)
st.link_button("View source on GitHub", "https://github.com/mukundnaramesh2605/Real-Estate-Investment-Advisor---Predicting-Property-Profitability-Future-Value", icon="🔗")

st.divider()
st.subheader("Pages")

st.page_link("pages/1_EDA Visualizations.py", label="EDA Visualization", icon="📊")
st.page_link("pages/2_Prediction.py", label="Price & Good Investment Precition", icon="💻")

