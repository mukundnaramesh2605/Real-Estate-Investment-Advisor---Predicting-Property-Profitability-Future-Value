import plotly.express as px
import streamlit as st
from helper_functions.dataset_reader import dataset_reader
from helper_functions.eda_helpers import PLOTLY_CONFIG


dr = dataset_reader()
df = dr.get_data()
st.set_page_config(page_title="EDA - Categorical Factors", page_icon="📊", layout="wide")

st.title("📊 EDA Visualizations — Location & Amenities Factors")

st.divider()
title_10 = 'Price per SqFt by Number of Nearby Schools'
st.subheader(title_10)
fig = px.box(data_frame=df,x='Nearby_Schools',y='Price_per_SqFt',color='Nearby_Schools',color_discrete_sequence=px.colors.sequential.Viridis)
fig.update_layout(
    title_text=title_10, # title of plot
    xaxis_title_text='Number of Nearby Schools', # xaxis label
    yaxis_title_text='Price per SqFt', # yaxis label
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True, key='chart_10', config=PLOTLY_CONFIG)


st.divider()
title_11 = 'Price per SqFt by Number of Nearby Hospitals'
st.subheader(title_11)
fig = px.box(data_frame=df,x='Nearby_Hospitals',y='Price_per_SqFt',color='Nearby_Hospitals',color_discrete_sequence=px.colors.sequential.Viridis)
fig.update_layout(
    title_text=title_11, # title of plot
    xaxis_title_text='Number of Nearby Hospitals', # xaxis label
    yaxis_title_text='Price per SqFt', # yaxis label
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True, key='chart_11', config=PLOTLY_CONFIG)


st.divider()
title_13 = 'Price per sqft by Facing Direction'
st.subheader(title_13)
fig = px.box(data_frame=df,x='Facing',y='Price_per_SqFt',color='Facing',color_discrete_sequence=px.colors.sequential.Blues)
fig.update_layout(
    title_text=title_13, # title of plot
    xaxis_title_text='Facing Direction', # xaxis label
    yaxis_title_text='Price per SqFt', # yaxis label
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True, key='chart_13', config=PLOTLY_CONFIG)


st.divider()
title_16 = 'Price per Sqft by Amenities'
st.subheader(title_16)
fig = px.box(data_frame=df,x='Amenities_Count',y='Price_per_SqFt',color='Amenities_Count',color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(
    title_text=title_16, # title of plot
    xaxis_title_text='Amenities_Count', # xaxis label
    yaxis_title_text='Price_per_SqFt', # yaxis label
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True, key='chart_16', config=PLOTLY_CONFIG)


st.divider()
title_18 = 'Price per Sqft by Public Transport Accessibility'
st.subheader(title_18)
fig = px.box(data_frame=df,x='Public_Transport_Accessibility',y='Price_per_SqFt',color='Public_Transport_Accessibility',color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(
    title_text=title_18, # title of plot
    xaxis_title_text='Public_Transport_Accessibility', # xaxis label
    yaxis_title_text='Price_per_SqFt', # yaxis label
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True, key='chart_18', config=PLOTLY_CONFIG)
