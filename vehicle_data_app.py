# Import libraries
import pandas as pd
import streamlit as st
import plotly_express as px

# App title
st.title("Vehicle Data Visualizer")

# App description
st.markdown("""
This app is an interactive data visualizer for the provided vehicle dataset.
            
The user is able to search and filter vehicles according to the specific data columns provided.
In addition there are several vehicle statistics charts provided for a broader visualization of data:
            
* **Python libraries:** pandas, streamlit, plotly express
""")

# Read dataframe
df = pd.read_csv('vehicles_us.csv')

# Add features: Manufacturer column
df['manufacturer'] = df['model'].str.split(' ').str[0]
df['model'] = df['model'].str.split(' ').str[1]

# Correct datatype and fill NaN values
df['cylinders'].fillna(0, inplace=True)
df['odometer'].fillna(0, inplace=True)
df['paint_color'].fillna('N/A', inplace=True)
df['is_4wd'].fillna(0, inplace=True)
df['model_year'].fillna(0, inplace=True)
df['model_year'] = df['model_year'].astype(int)
df['model_year'] = df['model_year'].astype(str)
df['model_year'] = df['model_year'].replace('0', 'N/A')

# Sidebar
st.sidebar.header('Vehicle Filter')

# Year selectbox 
selected_year = st.sidebar.selectbox('Year', options=['All'] + df['model_year'].sort_values(ascending=False).unique().tolist())

# Manufacturer multiselect 
selected_manufacturer = st.sidebar.multiselect('Manufacturer', options= df['manufacturer'].unique(), default=df['manufacturer'].unique())

# Type multiselect
selected_type = st.sidebar.multiselect('Type', options= df['type'].unique(), default=df['type'].unique())

# Filter button
fitler_button = st.sidebar.button('Filter')

# Filter function
@st.cache_data
def filter_data(df, year, manufacturer, type):
    if year != 'All':
        df = df[df['model_year'] == year]
    if manufacturer:
        df = df[df['manufacturer'].isin(manufacturer)]
    if type:
        df = df[df['type'].isin(type)]
    return df

# Apply filter 
if fitler_button:
    filtered_df = filter_data(df, selected_year, selected_manufacturer, selected_type)
else:
    filtered_df = df

# Dataframe header and dimension
st.header("Vehicle Data")
st.write('Data Dimension:  ' + str(filtered_df.shape[0]) + ' rows and ' + str(filtered_df.shape[1]) + ' columns.')

# Display dataframe
st.write(filtered_df)
st.write('Cylinders and Odometer 0 (zero) values represent no infomation available.')

# Vehicle types by manufaturer bar chart
st.header('Vehicle Types by Manufacturer')
df_make_type_bar = px.bar(df, x="manufacturer", color="type")
st.plotly_chart(df_make_type_bar)

#Vehicle condition vs model year histogram
st.header('Vehicle Condition vs. Model Year')
df_cond_year_hist = px.histogram(df, x="model_year", color="condition", labels=dict(model_year="Model year"))
st.plotly_chart(df_cond_year_hist)

#Vehicle Year vs. price scatterplot
st.header('Vehicle Year vs. Price')
df_price_year_scat = px.scatter(df, x='model_year', y='price', color='model', labels=dict(price="Price", model_year="Model year"))
st.plotly_chart(df_price_year_scat)
