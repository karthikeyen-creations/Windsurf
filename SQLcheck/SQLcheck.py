import streamlit as st
import re
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Updated regex patterns for DB2 queries
db2_update_pattern = re.compile(r'UPDATE\s+(\w+)\s+SET\s+([\s\S]+?)\s+WHERE', re.IGNORECASE)
db2_insert_pattern_values = re.compile(r'INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*SELECT\s*([\s\S]+?)\s+FROM', re.IGNORECASE)
db2_insert_pattern_simple = re.compile(r'INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\);', re.IGNORECASE)

# Function to extract DB2 queries
def extract_db2_queries(file_content):
    updates = []
    inserts = []

    # Extract UPDATE queries
    for match in db2_update_pattern.finditer(file_content):
        table_name = match.group(1)
        set_clause = match.group(2)
        column_value_pairs = []
        for pair in set_clause.split(','):
            column, value = pair.split('=')
            column_value_pairs.append((column.strip(), value.strip()))
        line_number = file_content[:match.start()].count('\n') + 1
        updates.append((table_name, column_value_pairs, line_number))
        print(f"Extracted DB2 UPDATE query for table {table_name} at line {line_number}")

    # Extract INSERT queries with SELECT
    for match in db2_insert_pattern_values.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        select_clause = match.group(3)
        select_values = select_clause.split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, select_values))
        inserts.append((table_name, column_value_pairs, line_number))
        print(f"Extracted DB2 INSERT SELECT query for table {table_name} at line {line_number}")

    # Extract simple INSERT queries with VALUES
    for match in db2_insert_pattern_simple.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        values = match.group(3).split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, values))
        inserts.append((table_name, column_value_pairs, line_number))
        print(f"Extracted DB2 INSERT VALUES query for table {table_name} at line {line_number}")

    return updates, inserts

# Updated regex patterns for Postgres queries
postgres_update_pattern = re.compile(r'UPDATE\s+(\w+\.\w+)\s+SET\s+([\s\S]+?)\s+WHERE', re.IGNORECASE)
postgres_insert_pattern_values = re.compile(r'INSERT\s+INTO\s+(\w+\.\w+)\s*\(([^)]+)\)\s*SELECT\s*([\s\S]+?)\s+FROM', re.IGNORECASE)
postgres_insert_pattern_simple = re.compile(r'INSERT\s+INTO\s+(\w+\.\w+)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\);', re.IGNORECASE)

# Function to extract Postgres queries
def extract_postgres_queries(file_content):
    updates = []
    inserts = []

    # Extract UPDATE queries
    for match in postgres_update_pattern.finditer(file_content):
        table_name = match.group(1)
        set_clause = match.group(2)
        column_value_pairs = []
        for pair in set_clause.split(','):
            column, value = pair.split('=')
            column_value_pairs.append((column.strip(), value.strip()))
        line_number = file_content[:match.start()].count('\n') + 1
        updates.append((table_name, column_value_pairs, line_number))
        print(f"Extracted Postgres UPDATE query for table {table_name} at line {line_number}")

    # Extract INSERT queries with SELECT
    for match in postgres_insert_pattern_values.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        select_clause = match.group(3)
        select_values = select_clause.split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, select_values))
        inserts.append((table_name, column_value_pairs, line_number))
        print(f"Extracted Postgres INSERT SELECT query for table {table_name} at line {line_number}")

    # Extract simple INSERT queries with VALUES
    for match in postgres_insert_pattern_simple.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        values = match.group(3).split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, values))
        inserts.append((table_name, column_value_pairs, line_number))
        print(f"Extracted Postgres INSERT VALUES query for table {table_name} at line {line_number}")

    return updates, inserts

# Function to store queries in a temporary SQLite table
def store_queries_in_db(conn, queries, query_type, source):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS query_data (
            id TEXT,
            line_number INTEGER,
            table_name TEXT,
            column_name TEXT,
            value TEXT,
            source TEXT
        )
    ''')

    # Insert data into the table
    for i, (table_name, column_value_pairs, line_number) in enumerate(queries, start=1):
        query_id = f"{query_type}_{i}"
        logger.info(f"Preparing to store {query_id}: Table {table_name}, Line {line_number}, Source {source}")
        logger.info(f"Column-Value Pairs: {column_value_pairs}")
        if isinstance(column_value_pairs, list):
            try:
                for column, value in column_value_pairs:
                    cursor.execute('INSERT INTO query_data (id, line_number, table_name, column_name, value, source) VALUES (?, ?, ?, ?, ?, ?)',
                                   (query_id, line_number, table_name, column.strip(), value.strip(), source))
                logger.info(f"Successfully stored {query_id}")
                # Debugging: Print all data in the database after each insertion
                fetch_all_data_from_db(conn)
            except sqlite3.Error as e:
                logger.error(f"Error storing {query_id}: {e}")
        else:
            logger.warning(f"Warning: Unexpected structure for column_value_pairs in {query_id}")

    conn.commit()

# Function to fetch data from the temporary SQLite table
def fetch_data_from_db(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT id, line_number, table_name, source FROM query_data')
    return cursor.fetchall()

# Function to fetch detailed data from the temporary SQLite table
def fetch_detailed_data_from_db(conn, query_id):
    cursor = conn.cursor()
    cursor.execute('SELECT column_name, value FROM query_data WHERE id = ?', (query_id,))
    return cursor.fetchall()

# Function to fetch all data from the temporary SQLite table for debugging
def fetch_all_data_from_db(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM query_data')
    all_data = cursor.fetchall()
    logger.info("All data in query_data table:")
    for row in all_data:
        logger.info(row)

# Streamlit app
def main():
    st.set_page_config(layout="wide")
    st.title("DB2 and Postgres Stored Procedure Query Extractor")
    st.write("Upload DB2 and Postgres stored procedure files to extract UPDATE and INSERT queries.")

    # File uploaders
    col1, col2 = st.columns(2)

    with col1:
        db2_file = st.file_uploader("Choose a DB2 file", type=["txt", "sql"], key="db2")
    with col2:
        postgres_file = st.file_uploader("Choose a Postgres file", type=["txt", "sql"], key="postgres")

    if db2_file and postgres_file:
        # Check if both files have the same name (case insensitive)
        if db2_file.name.lower() == postgres_file.name.lower():
            # Read file contents
            db2_content = db2_file.read().decode("utf-8")
            postgres_content = postgres_file.read().decode("utf-8")

            # Extract queries
            db2_updates, db2_inserts = extract_db2_queries(db2_content)
            postgres_updates, postgres_inserts = extract_postgres_queries(postgres_content)

            # Create a single connection for DB2
            db2_conn = sqlite3.connect(':memory:')
            store_queries_in_db(db2_conn, db2_updates, "update", "DB2")
            store_queries_in_db(db2_conn, db2_inserts, "insert", "DB2")

            # Create a single connection for Postgres
            postgres_conn = sqlite3.connect(':memory:')
            store_queries_in_db(postgres_conn, postgres_updates, "update", "Postgres")
            store_queries_in_db(postgres_conn, postgres_inserts, "insert", "Postgres")

            # Fetch and display data
            db2_data = fetch_data_from_db(db2_conn)
            postgres_data = fetch_data_from_db(postgres_conn)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("DB2 Queries")
                for row in db2_data:
                    st.write(f"{row[0]} (Line {row[1]}): {row[0].split('_')[0].upper()} {row[2]} [{row[3]}]")
                    detailed_data = fetch_detailed_data_from_db(db2_conn, row[0])
                    st.table(detailed_data)

            with col2:
                st.subheader("Postgres Queries")
                for row in postgres_data:
                    st.write(f"{row[0]} (Line {row[1]}): {row[0].split('_')[0].upper()} {row[2]} [{row[3]}]")
                    detailed_data = fetch_detailed_data_from_db(postgres_conn, row[0])
                    st.table(detailed_data)

        else:
            st.error("The file names do not match. Please upload files with the same name.")

if __name__ == "__main__":
    main()
