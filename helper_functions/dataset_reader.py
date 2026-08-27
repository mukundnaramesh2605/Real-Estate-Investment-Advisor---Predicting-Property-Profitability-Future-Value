import pandas as pd
import streamlit as st


@st.cache_data
def _load_dataset():
    return pd.read_csv(r'Datasets/india_housing_prices_with_target_columns.csv')


class dataset_reader:
    def __init__(self):
        self.df = _load_dataset()

    def get_data(self):
        return self.df