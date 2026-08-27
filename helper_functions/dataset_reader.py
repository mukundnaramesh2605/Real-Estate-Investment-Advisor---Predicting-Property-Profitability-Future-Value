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
        cities = sorted(self.df['City'].unique().tolist())
        return cities

    def get_property_type(self):
        property_types = sorted(self.df['Property_Type'].unique().tolist())
        return property_types

    def get_facing(self):
        facing = sorted(self.df['Facing'].unique().tolist())
        return facing

    def get_owner_type(self):
        owner_type = sorted(self.df['Owner_Type'].unique().tolist())
        return owner_type

    def get_avaialble_status(self):
        available_status = sorted(self.df['Availability_Status'].unique().tolist())
        return available_status