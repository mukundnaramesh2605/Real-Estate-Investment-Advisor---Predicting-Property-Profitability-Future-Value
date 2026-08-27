import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
from helper_functions.dataset_reader import dataset_reader
from helper_functions.eda_helpers import PLOTLY_CONFIG, get_value_counts, get_investment_rate


dr = dataset_reader()
df = dr.get_data()
st.set_page_config(page_title="EDA - Investment Factors", page_icon="📊", layout="wide")

st.title("📊 EDA Visualizations — Property & Investment Factors")

st.divider()
title_12 = 'Price by Furnished Status'
st.subheader(title_12)
fig = px.box(data_frame=df,x='Furnished_Status',y='Price_in_Lakhs',color='Furnished_Status',color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(
    title_text=title_12, # title of plot
    xaxis_title_text='Furnished Status', # xaxis label
    yaxis_title_text='Price (Lakhs)', # yaxis label
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True, key='chart_12', config=PLOTLY_CONFIG)


st.divider()
title_14 = 'Property Count by Owner Type'
st.subheader(title_14)
owner_counts = get_value_counts(df, 'Owner_Type')
fig = px.bar(data_frame=owner_counts,x='Owner_Type',y='Count',color='Owner_Type',text='Count')
fig.update_traces(textposition='outside')
fig.update_layout(
    title_text=title_14, # title of plot
    xaxis_title_text='Owner Type', # xaxis label
    yaxis_title_text='Count', # yaxis label
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True, key='chart_14', config=PLOTLY_CONFIG)


st.divider()
title_15 = 'Property Count by Availability Status'
st.subheader(title_15)
availability_counts = get_value_counts(df, 'Availability_Status')
fig = px.bar(data_frame=availability_counts,x='Availability_Status',y='Count',color='Availability_Status',text='Count')
fig.update_traces(textposition='outside')
fig.update_layout(
    title_text=title_15, # title of plot
    xaxis_title_text='Availability Status', # xaxis label
    yaxis_title_text='Count', # yaxis label
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True, key='chart_15', config=PLOTLY_CONFIG)


st.divider()
title_17 = 'Price by Parking Availability'
st.subheader(title_17)
fig = px.box(data_frame=df,x='Parking_Space',y='Price_in_Lakhs',color='Parking_Space',color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(
    title_text=title_17, # title of plot
    xaxis_title_text='Parking_Space', # xaxis label
    yaxis_title_text='Price_in_Lakhs', # yaxis label
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True, key='chart_17', config=PLOTLY_CONFIG)


st.divider()
title_20 = '% Good Investment by Key Factors'
st.subheader(title_20)
bhk_rate = get_investment_rate(df, 'BHK')
avail_rate = get_investment_rate(df, 'Availability_Status')
park_rate = get_investment_rate(df, 'Parking_Space')
amen_rate = get_investment_rate(df, 'Amenities_Count')

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        '% Good Investment by BHK',
        '% Good Investment by Availability',
        '% Good Investment by Parking',
        '% Good Investment by Amenities Count',
    ),
)
fig.add_bar(x=bhk_rate['BHK'], y=bhk_rate['Pct_Good'], marker_color='steelblue', row=1, col=1)
fig.add_bar(x=avail_rate['Availability_Status'], y=avail_rate['Pct_Good'], marker_color='seagreen', row=1, col=2)
fig.add_bar(x=park_rate['Parking_Space'], y=park_rate['Pct_Good'], marker_color='darkorange', row=2, col=1)
fig.add_bar(x=amen_rate['Amenities_Count'], y=amen_rate['Pct_Good'], marker_color='mediumpurple', row=2, col=2)
fig.add_hline(y=27.6, line_dash='dash', line_color='red', line_width=1, annotation_text='overall 27.6%', annotation_position='top left', row=1, col=1)
fig.update_yaxes(title_text='% Good', row=1, col=1)
fig.update_yaxes(title_text='% Good', row=1, col=2)
fig.update_yaxes(title_text='% Good', row=2, col=1)
fig.update_yaxes(title_text='% Good', row=2, col=2)
fig.update_layout(title_text=title_20, showlegend=False, height=700)
st.plotly_chart(fig, use_container_width=True, key='chart_20', config=PLOTLY_CONFIG)
