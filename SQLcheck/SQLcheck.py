import streamlit as st
import logging
from controllers.query_controller import QueryController
from daos.sqlite_dao import SQLiteDAO
import csv


logging.basicConfig(level=logging.INFO)

def main():
    st.set_page_config(layout="wide")
    st.title("DB2 and Postgres Stored Procedure Query Extractor")
    st.write("Upload DB2 and Postgres stored procedure files to extract UPDATE and INSERT queries.")

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
            db2_content = db2_file.read().decode("utf-8")
            postgres_content = postgres_file.read().decode("utf-8")

            # Initialize controllers
            query_controller = QueryController(db2_content, postgres_content)

            # Extract queries
            db2_updates, db2_inserts, postgres_updates, postgres_inserts = query_controller.extract_queries()

            # Store queries in the database
            sqlite_dao = SQLiteDAO()
            sqlite_dao.store_queries(db2_updates, "update", "DB2")
            sqlite_dao.store_queries(db2_inserts, "insert", "DB2")
            sqlite_dao.store_queries(postgres_updates, "update", "Postgres")
            sqlite_dao.store_queries(postgres_inserts, "insert", "Postgres")

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
    if 'db2_updates' in locals() and 'postgres_updates' in locals() and 'db2_inserts' in locals() and 'postgres_inserts' in locals():
        for i, ((db2_table, _, db2_line), (pg_table, _, pg_line)) in enumerate(zip(db2_updates, postgres_updates)):
            query_options.append(f"update{i+1} : (DB2 line: {db2_line}, postgres line: {pg_line}) UPDATE {db2_table}")
        for i, ((db2_table, _, db2_line), (pg_table, _, pg_line)) in enumerate(zip(db2_inserts, postgres_inserts)):
            query_options.append(f"insert{i+1} : (DB2 line: {db2_line}, postgres line: {pg_line}) INSERT INTO {db2_table}")

    logging.info(f"Generated query options: {query_options}")

    if query_options:
        selected_query = st.selectbox("Select a query to view details:", query_options)

        if selected_query:
            logging.info(f"Selected query ID: {selected_query.split(' ')[0]}")

            # Display the selected query's details using a database query
            query_id = selected_query.split(' ')[0]
            query_id = query_id.replace('update', 'update_').replace('insert', 'insert_')

            # Extract db2_table from selected_query
            db2_table = selected_query.split(' ')[-1]

            # Fetch detailed data with query_id and db2_table
            # detailed_data = sqlite_dao.fetch_query_details(query_id, db2_table)
            detailed_data = sqlite_dao.fetch_query_details(query_id, db2_table)
            logging.info(f"detailed_data: {detailed_data}")
            if detailed_data:
                st.table(detailed_data)
            else:
                st.write("No data found for the selected query.")
    else:
        st.write("No queries available for selection.")

    # Close the database connection
    # sqlite_dao.close()

if __name__ == "__main__":
    main()
