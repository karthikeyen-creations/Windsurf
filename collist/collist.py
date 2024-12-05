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

# Function to highlight missing datatype and length
# Highlight only if both column_datatype and column_length are empty
# or both COLTYPE and COLUMN_LENGTH are empty
# Additionally, highlight corresponding columns without '_db' or '_db2' suffix

def highlight_missing(row, data, highlight_list):
    highlight_color = ['background-color: #1E3A5F'] * len(row)
    secondary_highlight_color = ['background-color: #4B0082'] * len(row)
    # Initial highlighting condition
    if (pd.isna(row['column_datatype']) and pd.isna(row['column_length'])) or \
       (pd.isna(row['COLTYPE']) and pd.isna(row['COLUMN_LENGTH'])):
        if row['Column Name'].strip().lower().endswith('_db') or row['Column Name'].strip().lower().endswith('_db2'):
            base_column_name = row['Column Name'].strip().rsplit('_', 1)[0]
            # print(f"Column Name: *{base_column_name}*, {row['Table Name']}")
            # Add to highlight list
            highlight_list.append((base_column_name, row['Table Name']))
        return highlight_color
    # print(f"rem Column Name: *{row['Column Name']}*, {row['Table Name']}")    
    # Check if the combination is in the highlight list
    if (row['Column Name'], row['Table Name']) in highlight_list:
        # print(f"sel Column Name: *{row['Column Name']}*, {row['Table Name']}")    
        return secondary_highlight_color
    return [''] * len(row)

# Function to extract table names from SQL content
def extract_tables_from_sql(sql_content):
    # Regex to find tables in tgabm00 schema
    table_pattern = r'tgabm00\.(?:t\w+?_)?(\w+)'
    tables = list(set(re.findall(table_pattern, sql_content, re.IGNORECASE)))
    return tables

# Function to prepare the highlight list
# This function will populate the highlight_list based on the conditions

def prepare_highlight_list(data):
    highlight_list = []
    for _, row in data.iterrows():
        if (pd.isna(row['column_datatype']) and pd.isna(row['column_length'])) or \
           (pd.isna(row['COLTYPE']) and pd.isna(row['COLUMN_LENGTH'])):
            if row['Column Name'].strip().lower().endswith('_db') or row['Column Name'].strip().lower().endswith('_db2'):
                base_column_name = row['Column Name'].strip().rsplit('_', 1)[0]
                highlight_list.append((base_column_name, row['Table Name']))
    return highlight_list

# Main function to run the Streamlit app
def main():
    st.set_page_config(layout="wide", page_title="Postgres SQL Tables and Columns", page_icon="📊")  # Set app layout to wide
    st.title('Postgres SQL Tables and Columns')
    
    # File uploader for PostgreSQL function
    uploaded_file = st.sidebar.file_uploader("Upload a PostgreSQL function file", type=["sql"])
    
    # List table names below the file selection field
    if uploaded_file is not None:
        sql_content = uploaded_file.read().decode('utf-8')
        tables_in_sql = extract_tables_from_sql(sql_content)
        st.sidebar.write("**Tables in Uploaded SQL File:**")
        for table in tables_in_sql:
            st.sidebar.write(f"- {table}")
        # Reset file content for further processing
        uploaded_file.seek(0)

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

    # Add a checkbox for displaying only secondary highlighted rows
    show_secondary_highlighted = st.sidebar.checkbox('Show only secondary highlighted rows')

    # Prepare the highlight list
    highlight_list = prepare_highlight_list(merged_data)

    # Filter the data based on the checkboxes
    if show_secondary_highlighted and show_highlighted:
        # Combine both highlighted and secondary highlighted
        highlighted_mask = (
            (merged_data['column_datatype'].isna() & merged_data['column_length'].isna()) |
            (merged_data['COLTYPE'].isna() & merged_data['COLUMN_LENGTH'].isna())
        )
        secondary_highlighted_mask = merged_data.apply(lambda row: (row['Column Name'], row['Table Name']) in highlight_list, axis=1)
        combined_mask = highlighted_mask | secondary_highlighted_mask
        filtered_data = merged_data[combined_mask]
    elif show_secondary_highlighted:
        secondary_highlighted_mask = merged_data.apply(lambda row: (row['Column Name'], row['Table Name']) in highlight_list, axis=1)
        filtered_data = merged_data[secondary_highlighted_mask]
    elif show_highlighted:
        highlighted_mask = (
            (merged_data['column_datatype'].isna() & merged_data['column_length'].isna()) |
            (merged_data['COLTYPE'].isna() & merged_data['COLUMN_LENGTH'].isna())
        )
        filtered_data = merged_data[highlighted_mask]
    else:
        filtered_data = merged_data

    # Ensure column lengths are integers and replace NaNs with None
    filtered_data.loc[:, 'column_length'] = filtered_data['column_length'].apply(lambda x: None if pd.isna(x) else int(x) if x != 0 else None)
    filtered_data.loc[:, 'COLUMN_LENGTH'] = filtered_data['COLUMN_LENGTH'].apply(lambda x: None if pd.isna(x) else int(x) if x != 0 else None)

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
        st.dataframe(filtered_data[['File Name', 'Table Name', 'Column Name', 'column_datatype', 'column_length', 'COLTYPE', 'COLUMN_LENGTH']].style.apply(lambda row: highlight_missing(row, filtered_data, highlight_list), axis=1))
    else:
        st.dataframe(filtered_data[['Table Name', 'Column Name', 'column_datatype', 'column_length', 'COLTYPE', 'COLUMN_LENGTH']].style.apply(lambda row: highlight_missing(row, filtered_data, highlight_list), axis=1))

    # Button to copy CSV format of the displayed list
    if st.button('Copy CSV to Clipboard'):
        csv_data = filtered_data.to_csv(index=False)
        st.write('CSV data copied to clipboard!')
        st.code(csv_data, language='csv')

    # Button to copy CSV format without headers
    if st.button('Copy CSV without Headers'):
        csv_data_no_headers = filtered_data.to_csv(index=False, header=False)
        st.write('CSV data without headers copied to clipboard!')
        st.code(csv_data_no_headers, language='csv')

if __name__ == '__main__':
    main()
