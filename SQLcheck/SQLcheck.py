import streamlit as st
import logging
from controllers.query_controller import QueryController
from daos.sqlite_dao import SQLiteDAO
import csv
import pandas as pd
import re


logging.basicConfig(level=logging.INFO)

def main():
    st.set_page_config(layout="wide")
    st.title("DB2 and Postgres Stored Procedure Query Extractor")
    st.write("Upload DB2 and Postgres stored procedure files to extract UPDATE, INSERT, and SELECT queries.")

    # File uploaders with condition to disable after loading
    col1, col2 = st.columns(2)

    with col1:
        db2_file = st.file_uploader("Choose a DB2 file", type=["txt", "sql"], key="db2", disabled=st.session_state.get('files_loaded', False))
    with col2:
        postgres_file = st.file_uploader("Choose a Postgres file", type=["txt", "sql"], key="postgres", disabled=st.session_state.get('files_loaded', False))

    if db2_file and postgres_file:
        # Mark files as loaded
        st.session_state['files_loaded'] = True

        # Check if both files have the same name (case insensitive)
        if db2_file.name.lower() == postgres_file.name.lower():
            # Read file contents
            db2_content = "\n".join([line for line in db2_file.read().decode("utf-8").splitlines() if not line.strip().startswith("--")])
            postgres_content = "\n".join([line for line in postgres_file.read().decode("utf-8").splitlines() if not line.strip().startswith("--")])

            # Initialize controllers
            query_controller = QueryController(db2_content, postgres_content)

            # Extract queries
            db2_update_pattern = re.compile(r'UPDATE\s+(\w+)(?:\s+\w+)?\s+SET\s+([\s\S]+?)(?:\s+WHERE|\s*;)', re.IGNORECASE)
            db2_insert_pattern_values = re.compile(r'INSERT\s+INTO\s+(\w+)(?:\s+\w+)?\s*\(([^)]+)\)\s*SELECT\s*([\s\S]+?)\s+FROM', re.IGNORECASE)
            db2_insert_pattern_simple = re.compile(r'INSERT\s+INTO\s+(\w+)(?:\s+\w+)?\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\);', re.IGNORECASE)

            db2_updates, db2_inserts, postgres_updates, postgres_inserts, db2_selects, postgres_selects = query_controller.extract_queries(db2_update_pattern, db2_insert_pattern_values, db2_insert_pattern_simple)

            # Store queries in the database
            sqlite_dao = SQLiteDAO()
            sqlite_dao.store_queries(db2_updates, "update", "DB2")
            sqlite_dao.store_queries(db2_inserts, "insert", "DB2")
            
            # logging.info(f"db2_inserts: {db2_inserts}")
            sqlite_dao.store_queries(db2_selects, "select", "DB2")
            
            # # Store select queries and their column names
            # for i, (table_name, query, line_number) in enumerate(db2_selects, start=1):
            #     query = 'SELECT ' + query + ' FROM ' + table_name
            #     query_id = f"select_{i}"
            #     logging.info(f"Extracting column names from query: {query}")
            #     # match = re.search(r'SELECT\s+(.+?)\s+FROM', query, re.IGNORECASE)
            #     match = re.search(r'SELECT\s+([\s\S]+?)\s+FROM', query, re.IGNORECASE)
            #     logging.info(f"Match: {match}")
            #     if match:
            #         column_names = [col.strip() for col in match.group(1).split(',')]
            #         logging.info(f"Identified column names: {column_names}")
            #         sqlite_dao.store_queries([(table_name, [(str(i), col) for i, col in enumerate(column_names)], line_number)], "select_columns", "DB2")
            #     else:
            #         logging.info(f"No column names found for query: {query}")
            
            sqlite_dao.store_queries(postgres_updates, "update", "Postgres")
            sqlite_dao.store_queries(postgres_inserts, "insert", "Postgres")
            # logging.info(f"postgres_updates: {postgres_updates}")
            logging.info(f"db2_selects: {db2_selects}")
            logging.info(f"postgres_selects: {postgres_selects}")
            sqlite_dao.store_queries(postgres_selects, "select", "Postgres")

            # Read CSV file and store data into SQLite

            csv_path = 'SQLcheck/columns/DA73_tables_columns.csv'
            with open(csv_path, mode='r', newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                csv_data = [(row['TNAME'], row['NAME'], row['COLTYPE'], row['COLUMN_LENGTH']) for row in csv_reader]

            # Store CSV data into SQLite
            sqlite_dao.store_csv_data(csv_data)

            # Read second CSV file and store data into SQLite
            csv_path_postgres = 'SQLcheck/columns/tgabm00_tables_columns.csv'
            with open(csv_path_postgres, mode='r', newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                csv_data_postgres = [(row['t_name'], row['column_name'], row['column_datatype'], row['column_length']) for row in csv_reader]

            # Store CSV data into SQLite
            sqlite_dao.store_csv_data(csv_data_postgres, source='Postgres')

            # # Fetch and display all data
            # logging.info("Fetching all data with query: SELECT * FROM query_data")
            # all_data = sqlite_dao.fetch_all_data()
            # for row in all_data:
            #     st.write(row)

        else:
            st.error("The file names do not match. Please upload files with the same name.")

    # Create dropdown for query selection with updated format
    query_options = []
    if 'db2_updates' in locals() and 'postgres_updates' in locals() and 'db2_inserts' in locals() and 'postgres_inserts' in locals() and 'db2_selects' in locals() and 'postgres_selects' in locals():
        for i, ((db2_table, _, db2_line), (pg_table, _, pg_line)) in enumerate(zip(db2_updates, postgres_updates)):
            query_options.append(f"update{i+1} : (DB2 line: {db2_line}, postgres line: {pg_line}) UPDATE {db2_table}")
        for i, ((db2_table, _, db2_line), (pg_table, _, pg_line)) in enumerate(zip(db2_inserts, postgres_inserts)):
            query_options.append(f"insert{i+1} : (DB2 line: {db2_line}, postgres line: {pg_line}) INSERT INTO {db2_table}")
        for i, ((db2_table, _, db2_line), (pg_table, _, pg_line)) in enumerate(zip(db2_selects, postgres_selects)):
            query_options.append(f"select{i+1} : (DB2 line: {db2_line}, postgres line: {pg_line}) SELECT {db2_table}")


    logging.info(f"Generated query options: {query_options}")

    if query_options:
        selected_query = st.selectbox("Select a query to view details:", query_options)

        if selected_query:
            logging.info(f"Selected query ID: {selected_query.split(' ')[0]}")

            # Display the selected query's details using a database query
            query_id = selected_query.split(' ')[0]
            query_id = query_id.replace('update', 'update_').replace('insert', 'insert_').replace('select', 'select_')

            # Extract db2_table from selected_query
            db2_table = selected_query.split(' ')[-1]
            
            # Fetch detailed data with query_id and db2_table
            detailed_data = sqlite_dao.fetch_query_details(query_id, db2_table)
            logging.info(f"detailed_data: {detailed_data}")
            if detailed_data:
                # Display detailed data with column names
                column_names = ["PGcsv", "DB2csv", "Column Name", "DB2 Value", "Postgres Value", "Match"]
                styled_df = pd.DataFrame(detailed_data, columns=column_names).style

                # Apply conditional formatting to highlight 'No Match' and None rows with dark theme colors
                def highlight_rows(row):
                    color = ''
                    if row['Match'] == 'No Match':
                        color = 'background-color: #5a2a2a'  # dark red
                    elif pd.isnull(row['Match']):
                        color = 'background-color: #2a2a5a'  # dark blue
                    return [color] * len(row)

                styled_df = styled_df.apply(highlight_rows, axis=1)

                styled_df = styled_df.set_table_styles(
                    [{'selector': 'thead th', 'props': [('background-color', '#333'), ('color', 'white'), ('font-size', '12px'), ('padding', '4px')]},
                     {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#444'), ('color', 'white'), ('font-size', '12px'), ('padding', '4px')]},
                     {'selector': 'tbody tr:nth-child(odd)', 'props': [('background-color', '#555'), ('color', 'white'), ('font-size', '12px'), ('padding', '4px')]},
                     {'selector': 'tbody tr:hover', 'props': [('background-color', '#666')]}]
                )
                st.write(styled_df.to_html(), unsafe_allow_html=True)
            else:
                st.write("No data found for the selected query.")
    else:
        st.write("No queries available for selection.")

    # Close the database connection
    # sqlite_dao.close()

if __name__ == "__main__":
    main()
