import plotly.express as px
import streamlit as st
from helper_functions.dataset_reader import dataset_reader
from helper_functions.eda_helpers import (
    PLOTLY_CONFIG,
    get_bhk_by_city,
    get_locality_trend,
    get_numeric_corr,
    get_target_corr,
)


dr = dataset_reader()
df = dr.get_data()
st.set_page_config(page_title="EDA - Correlations", page_icon="📊", layout="wide")

st.title("📊 EDA Visualizations — Relationships & Correlations")

st.divider()
title_7 = 'BHK Distribution Across Cities'
st.subheader(title_7)
bhk_by_city = get_bhk_by_city(df)
fig = px.bar(data_frame=bhk_by_city,x='City',y='Count',color='BHK',barmode='stack')
fig.update_layout(
    title_text=title_7, # title of plot
    xaxis_title_text='City', # xaxis label
    yaxis_title_text='Number of Properties', # yaxis label
    legend_title_text='BHK',
)
st.plotly_chart(fig, use_container_width=True, key='chart_7', config=PLOTLY_CONFIG)


st.divider()
title_8 = 'Price by Build Year — Top 5 Most Expensive Localities'
st.subheader(title_8)
trend = get_locality_trend(df)
fig = px.line(data_frame=trend,x='Year_Built',y='Price_in_Lakhs',color='Locality')
fig.update_layout(
    title_text=title_8, # title of plot
    xaxis_title_text='Year Built (proxy for time)', # xaxis label
    yaxis_title_text='Avg Price (Lakhs)', # yaxis label
    legend_title_text='Locality',
)
st.plotly_chart(fig, use_container_width=True, key='chart_8', config=PLOTLY_CONFIG)


st.divider()
title_9 = 'Correlation of Original Numeric Features'
st.subheader(title_9)
corr = get_numeric_corr(df)
fig = px.imshow(corr,text_auto='.2f',color_continuous_scale='RdBu_r',zmin=-1,zmax=1,aspect='auto')
fig.update_layout(
    title_text=title_9, # title of plot
)
st.plotly_chart(fig, use_container_width=True, key='chart_9', config=PLOTLY_CONFIG)


st.divider()
title_19 = 'Correlation of Numerical Features with Future_Price_5Y'
st.subheader(title_19)
target_corr = get_target_corr(df)
fig = px.bar(data_frame=target_corr,x='Correlation',y='Feature',orientation='h',color='Correlation',color_continuous_scale='RdBu_r')
fig.add_vline(x=0, line_dash='dash', line_color='gray')
fig.update_layout(
    title_text=title_19, # title of plot
    xaxis_title_text='Correlation Coefficient (r)', # xaxis label
    yaxis_title_text='Features', # yaxis label
)
st.plotly_chart(fig, use_container_width=True, key='chart_19', config=PLOTLY_CONFIG)
