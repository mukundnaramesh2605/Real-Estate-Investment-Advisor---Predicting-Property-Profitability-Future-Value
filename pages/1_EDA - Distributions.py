import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
from helper_functions.dataset_reader import dataset_reader
from helper_functions.eda_helpers import PLOTLY_CONFIG


dr = dataset_reader()
df = dr.get_data()
st.set_page_config(page_title="EDA - Distributions", page_icon="📊", layout="wide")

st.title("📊 EDA Visualizations — Distributions & Outliers")

st.divider()
title_1 = 'Property Price Distribution'
st.subheader(title_1)
fig = px.histogram(data_frame=df,x='Price_in_Lakhs',nbins=50)
fig.update_layout(
    title_text=title_1, # title of plot
    xaxis_title_text='Price_in_Lakhs', # xaxis label
    yaxis_title_text='Count', # yaxis label
    bargap=0.2,
    bargroupgap=0.1
)
st.plotly_chart(fig, use_container_width=True, key='chart_1', config=PLOTLY_CONFIG)

st.divider()
title_2 = 'Property Size Distribution'
st.subheader(title_2)
fig = px.histogram(data_frame=df,x='Size_in_SqFt',nbins=50)
fig.update_layout(
    title_text=title_2, # title of plot
    xaxis_title_text='Size_in_SqFt', # xaxis label
    yaxis_title_text='Count', # yaxis label
    bargap=0.2,
    bargroupgap=0.1
)
st.plotly_chart(fig, use_container_width=True, key='chart_2', config=PLOTLY_CONFIG)


st.divider()
title_3 = 'Price per SqFt by Property Type'
st.subheader(title_3)
fig = px.box(data_frame=df,y='Property_Type',x='Price_per_SqFt')
fig.update_layout(
    title_text=title_3, # title of plot
    xaxis_title_text='Price_per_SqFt', # xaxis label
    yaxis_title_text='Property_Type', # yaxis label
    bargap=0.2,
    bargroupgap=0.1
)
st.plotly_chart(fig, use_container_width=True, key='chart_3', config=PLOTLY_CONFIG)


st.divider()
title_4 = 'Relationship between Property Size and Price'
st.subheader(title_4)
fig = px.box(data_frame=df,y='Price_in_Lakhs',x='Size_in_SqFt')
fig.update_layout(
    title_text=title_4, # title of plot
    xaxis_title_text='Size_in_SqFt', # xaxis label
    yaxis_title_text='Price_in_Lakhs', # yaxis label
    bargap=0.2,
    bargroupgap=0.1
)
st.plotly_chart(fig, use_container_width=True, key='chart_4', config=PLOTLY_CONFIG)


st.divider()
title_6 = 'Outliers in Price per SqFt and Property Size'
st.subheader(title_6)
fig = make_subplots(rows=1, cols=2, subplot_titles=('Outlier in Price per SqFt', 'Outlier in Property Size'))
fig.add_box(y=df['Price_per_SqFt'], name='Price_per_SqFt', marker_color='coral', row=1, col=1)
fig.add_box(y=df['Size_in_SqFt'], name='Size_in_SqFt', marker_color='coral', row=1, col=2)
fig.update_layout(title_text=title_6, showlegend=False)
st.plotly_chart(fig, use_container_width=True, key='chart_6', config=PLOTLY_CONFIG)
