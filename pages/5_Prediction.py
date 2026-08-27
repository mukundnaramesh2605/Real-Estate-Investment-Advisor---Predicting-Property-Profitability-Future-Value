import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
from helper_functions.dataset_reader import dataset_reader

st.set_page_config(page_title="Predictions", page_icon="💻", layout="wide")

st.title("💻 Predictions")

dr = dataset_reader()

city = dr.get_cities()
st.write(city)