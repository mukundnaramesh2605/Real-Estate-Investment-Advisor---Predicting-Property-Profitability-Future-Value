import streamlit as st


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
