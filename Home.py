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

st.page_link("pages/1_EDA - Distributions.py", label="EDA: Distributions & Outliers", icon="📊")
st.page_link("pages/2_EDA - Correlations.py", label="EDA: Relationships & Correlations", icon="📊")
st.page_link("pages/3_EDA - Categorical Factors.py", label="EDA: Location & Amenities Factors", icon="📊")
st.page_link("pages/4_EDA - Investment Factors.py", label="EDA: Property & Investment Factors", icon="📊")
st.page_link("pages/5_Prediction.py", label="Price & Good Investment Precition", icon="💻")

