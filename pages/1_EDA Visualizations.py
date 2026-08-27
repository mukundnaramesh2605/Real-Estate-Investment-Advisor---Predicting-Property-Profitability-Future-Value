import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
from helper_functions.dataset_reader import dataset_reader


PLOTLY_CONFIG = {'displayModeBar': False}


@st.cache_data
def get_bhk_by_city(df):
    return df.groupby(['City', 'BHK']).size().reset_index(name='Count')


@st.cache_data
def get_locality_trend(df):
    top5 = df.groupby('Locality')['Price_in_Lakhs'].mean().nlargest(5).index
    sub = df[df['Locality'].isin(top5)]
    return sub.groupby(['Year_Built', 'Locality'])['Price_in_Lakhs'].mean().reset_index()


@st.cache_data
def get_numeric_corr(df):
    exclude = ['Growth_Rate_Annual', 'Future_Price_5Y', 'Good_Investment']
    num = df.select_dtypes(include='number').drop(columns=exclude, errors='ignore')
    return num.corr()


@st.cache_data
def get_value_counts(df, column):
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, 'Count']
    return counts


@st.cache_data
def get_target_corr(df):
    target_corr = df.corr(numeric_only=True)['Future_Price_5Y'].drop(['Future_Price_5Y', 'Good_Investment']).sort_values().reset_index()
    target_corr.columns = ['Feature', 'Correlation']
    return target_corr


@st.cache_data
def get_investment_rate(df, column):
    return (df.groupby(column)['Good_Investment'].mean() * 100).reset_index(name='Pct_Good')


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
