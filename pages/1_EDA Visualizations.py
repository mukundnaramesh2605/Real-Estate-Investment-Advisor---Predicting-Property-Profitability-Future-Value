import plotly.express as px
import streamlit as st
from helper_functions.dataset_reader import dataset_reader


dr = dataset_reader()
df = dr.get_data()
st.set_page_config(page_title="EDA Visualizations", page_icon="📊", layout="wide")

st.title("📊 EDA Visualizations")

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
st.plotly_chart(fig, use_container_width=True, key='chart_1')

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
st.plotly_chart(fig, use_container_width=True, key='chart_2')


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
st.plotly_chart(fig, use_container_width=True, key='chart_3')


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
st.plotly_chart(fig, use_container_width=True, key='chart_4')


st.divider()
title_5 = 'Relationship between Property Size and Price'
st.subheader(title_5)
fig = px.box(data_frame=df,y='Price_in_Lakhs',x='Size_in_SqFt')
fig.update_layout(
    title_text=title_5, # title of plot
    xaxis_title_text='Size_in_SqFt', # xaxis label
    yaxis_title_text='Price_in_Lakhs', # yaxis label
    bargap=0.2,
    bargroupgap=0.1
)
st.plotly_chart(fig, use_container_width=True, key='chart_5')


st.divider()
title_6 = 'Outliers in Price per SqFt and Property Size'
st.subheader(title_6)
col1, col2 = st.columns(2)

with col1:
    fig = px.box(data_frame=df,y='Price_per_SqFt')
    fig.update_layout(
        title_text='Outlier in Price per SqFt', # title of plot
        yaxis_title_text='Price_per_SqFt', # yaxis label
    )
    fig.update_traces(marker_color='coral')
    st.plotly_chart(fig, use_container_width=True, key='chart_6a')

with col2:
    fig = px.box(data_frame=df,y='Size_in_SqFt')
    fig.update_layout(
        title_text='Outlier in Property Size', # title of plot
        yaxis_title_text='Size_in_SqFt', # yaxis label
    )
    fig.update_traces(marker_color='coral')
    st.plotly_chart(fig, use_container_width=True, key='chart_6b')


st.divider()
title_7 = 'BHK Distribution Across Cities'
st.subheader(title_7)
bhk_by_city = df.groupby(['City', 'BHK']).size().reset_index(name='Count')
fig = px.bar(data_frame=bhk_by_city,x='City',y='Count',color='BHK',barmode='stack')
fig.update_layout(
    title_text=title_7, # title of plot
    xaxis_title_text='City', # xaxis label
    yaxis_title_text='Number of Properties', # yaxis label
    legend_title_text='BHK',
)
st.plotly_chart(fig, use_container_width=True, key='chart_7')


st.divider()
title_8 = 'Price by Build Year — Top 5 Most Expensive Localities'
st.subheader(title_8)
top5 = df.groupby('Locality')['Price_in_Lakhs'].mean().nlargest(5).index
sub = df[df['Locality'].isin(top5)]
trend = sub.groupby(['Year_Built', 'Locality'])['Price_in_Lakhs'].mean().reset_index()
fig = px.line(data_frame=trend,x='Year_Built',y='Price_in_Lakhs',color='Locality')
fig.update_layout(
    title_text=title_8, # title of plot
    xaxis_title_text='Year Built (proxy for time)', # xaxis label
    yaxis_title_text='Avg Price (Lakhs)', # yaxis label
    legend_title_text='Locality',
)
st.plotly_chart(fig, use_container_width=True, key='chart_8')


st.divider()
title_9 = 'Correlation of Original Numeric Features'
st.subheader(title_9)
exclude = ['Growth_Rate_Annual', 'Future_Price_5Y', 'Good_Investment']
num = df.select_dtypes(include='number').drop(columns=exclude, errors='ignore')
corr = num.corr()
fig = px.imshow(corr,text_auto='.2f',color_continuous_scale='RdBu_r',zmin=-1,zmax=1,aspect='auto')
fig.update_layout(
    title_text=title_9, # title of plot
)
st.plotly_chart(fig, use_container_width=True, key='chart_9')


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
st.plotly_chart(fig, use_container_width=True, key='chart_10')


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
st.plotly_chart(fig, use_container_width=True, key='chart_11')


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
st.plotly_chart(fig, use_container_width=True, key='chart_12')


