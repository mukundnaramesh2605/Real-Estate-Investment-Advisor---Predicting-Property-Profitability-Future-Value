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

    def get_cities(self):
        cities = self.df['City'].unique()
        return cities.tolist()

    def get_property_type(self):
        property_types = self.df['Property_Type'].unique()
        return property_types.tolist()

    def get_facing(self):
        facing = self.df['Facing'].unique()
        return facing.tolist()

    def get_owner_type(self):
        owner_type = self.df['Owner_Type'].unique()
        return owner_type.tolist()

    def get_avaialble_status(self):
        available_status = self.f['Availability_Status'].unique()
        return available_status.tolist()