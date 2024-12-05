import streamlit as st
import pandas as pd
import re

# Load the CSV files
def load_data():
    file_path_1 = 'collist/columns/tgabm00_tables_columns.csv'
    file_path_2 = 'collist/columns/DA73_tables_columns.csv'
    data_1 = pd.read_csv(file_path_1)
    data_2 = pd.read_csv(file_path_2)
    return data_1, data_2

# Function to highlight missing columns
def highlight_missing(row):
    style = [''] * len(row)
    # Highlight if both datatype and length are empty
    if pd.isna(row['column_datatype']) and pd.isna(row['column_length']):
        style[1] = 'background-color: #4B0082; color: #FFFFFF'  # Dark violet for column name
        style[2] = 'background-color: #1E3A5F; color: #FFFFFF'
        style[3] = 'background-color: #1E3A5F; color: #FFFFFF'
    if pd.isna(row['COLTYPE']) and pd.isna(row['COLUMN_LENGTH']):
        style[1] = 'background-color: #4B0082; color: #FFFFFF'
        style[4] = 'background-color: #1E3A5F; color: #FFFFFF'
        style[5] = 'background-color: #1E3A5F; color: #FFFFFF'
    return style

# Function to extract table names from SQL content
def extract_tables_from_sql(sql_content):
    # Regex to find tables in tgabm00 schema
    table_pattern = r'tgabm00\.(\w+)'
    tables = list(set(re.findall(table_pattern, sql_content, re.IGNORECASE)))
    return tables

# Main function to run the Streamlit app
def main():
    st.set_page_config(layout="wide", page_title="Postgres SQL Tables and Columns", page_icon="📊")  # Set app layout to wide
    st.title('Postgres SQL Tables and Columns')
    
    # File uploader for PostgreSQL function
    uploaded_file = st.sidebar.file_uploader("Upload a PostgreSQL function file", type=["sql"])
    
    # Load data
    data_1, data_2 = load_data()
    
    # Convert to lowercase for case-insensitive comparison
    data_1['t_name'] = data_1['t_name'].str.lower()
    data_1['column_name'] = data_1['column_name'].str.lower()
    data_2['TNAME'] = data_2['TNAME'].str.lower()
    data_2['NAME'] = data_2['NAME'].str.lower()
    
    # Merge data on table name and column name (case insensitive)
    merged_data = pd.merge(data_1, data_2, how='outer',
                           left_on=['t_name', 'column_name'],
                           right_on=['TNAME', 'NAME'],
                           suffixes=('_tgabm00', '_DA73'),
                           indicator=True)

    # Coalesce-like approach for table and column names
    merged_data['Table Name'] = merged_data['t_name'].combine_first(merged_data['TNAME'])
    merged_data['Column Name'] = merged_data['column_name'].combine_first(merged_data['NAME'])

    # If a file is uploaded, filter tables based on the file
    if uploaded_file is not None:
        sql_content = uploaded_file.read().decode('utf-8')
        tables_in_sql = extract_tables_from_sql(sql_content)
        merged_data = merged_data[merged_data['t_name'].isin(tables_in_sql)]
        # Add a column with the file name as the first column
        merged_data.insert(0, 'File Name', uploaded_file.name)

    # Add a checkbox for displaying only highlighted rows
    show_highlighted = st.sidebar.checkbox('Show only highlighted rows')

    # Filter the data based on the checkbox
    if show_highlighted:
        highlighted_mask = (
            (merged_data['column_datatype'].isna() & merged_data['column_length'].isna()) |
            (merged_data['COLTYPE'].isna() & merged_data['COLUMN_LENGTH'].isna())
        )
        filtered_data = merged_data[highlighted_mask]
    else:
        filtered_data = merged_data

    # Add filter dropdowns in the sidebar
    table_filter = st.sidebar.multiselect('Filter by Table Name', options=filtered_data['Table Name'].unique(), default=filtered_data['Table Name'].unique())
    column_filter = st.sidebar.multiselect('Filter by Column Name', options=filtered_data['Column Name'].unique(), default=filtered_data['Column Name'].unique())
    datatype_filter = st.sidebar.multiselect('Filter by Column Datatype', options=filtered_data['column_datatype'].unique(), default=filtered_data['column_datatype'].unique())
    coltype_filter = st.sidebar.multiselect('Filter by COLTYPE', options=filtered_data['COLTYPE'].unique(), default=filtered_data['COLTYPE'].unique())

    # Apply filters
    filtered_data = filtered_data[
        filtered_data['Table Name'].isin(table_filter) &
        filtered_data['Column Name'].isin(column_filter) &
        filtered_data['column_datatype'].isin(datatype_filter) &
        filtered_data['COLTYPE'].isin(coltype_filter)
    ]

    # Display the filtered data as a table
    st.write('Filtered Tables and Columns:')
    if 'File Name' in filtered_data.columns:
        st.dataframe(filtered_data[['File Name', 'Table Name', 'Column Name', 'column_datatype', 'column_length', 'COLTYPE', 'COLUMN_LENGTH']].style.apply(highlight_missing, axis=1))
    else:
        st.dataframe(filtered_data[['Table Name', 'Column Name', 'column_datatype', 'column_length', 'COLTYPE', 'COLUMN_LENGTH']].style.apply(highlight_missing, axis=1))

if __name__ == '__main__':
    main()
