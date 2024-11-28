import streamlit as st
import re

# Function to extract UPDATE and INSERT queries from the stored procedure content
def extract_queries(file_content):
    # Refined regex patterns to capture DB2 queries
    update_pattern = re.compile(r'UPDATE\s+(\w+)\s+SET\s+([\s\S]+?)\s+WHERE', re.IGNORECASE)
    insert_pattern_values = re.compile(r'INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\)', re.IGNORECASE)
    insert_pattern_select = re.compile(r'INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*SELECT\s+([\s\S]+?)\s+FROM', re.IGNORECASE)

    updates = []
    inserts = []

    # Extract UPDATE queries, table names, and their column-value pairs
    for match in update_pattern.finditer(file_content):
        table_name = match.group(1)
        column_value_pairs = match.group(2)
        line_number = file_content[:match.start()].count('\n') + 1
        updates.append((table_name, column_value_pairs, line_number))

    # Extract INSERT queries using VALUES
    for match in insert_pattern_values.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        values = match.group(3).split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        inserts.append((table_name, list(zip(columns, values)), line_number))

    # Extract INSERT queries using SELECT
    for match in insert_pattern_select.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        values = match.group(3).split(',')  # Simplified case for demonstration
        line_number = file_content[:match.start()].count('\n') + 1
        inserts.append((table_name, list(zip(columns, values)), line_number))

    return updates, inserts

# Function to extract UPDATE and INSERT queries from Postgres stored procedure content
def extract_postgres_queries(file_content):
    # Further refined regex patterns to capture all INSERT statements
    update_pattern = re.compile(r'UPDATE\s+(\w+)\s+SET\s+([\s\S]+?)\s+WHERE', re.IGNORECASE)
    insert_pattern_values = re.compile(r'INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\)', re.IGNORECASE)
    insert_pattern_select = re.compile(r'INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*SELECT\s+([\s\S]+?)\s+FROM', re.IGNORECASE)

    updates = []
    inserts = []

    # Extract UPDATE queries, table names, and their column-value pairs
    for match in update_pattern.finditer(file_content):
        table_name = match.group(1)
        column_value_pairs = match.group(2)
        line_number = file_content[:match.start()].count('\n') + 1
        updates.append((table_name, column_value_pairs, line_number))

    # Extract INSERT queries using VALUES
    for match in insert_pattern_values.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        values = match.group(3).split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        inserts.append((table_name, list(zip(columns, values)), line_number))

    # Extract INSERT queries using SELECT
    for match in insert_pattern_select.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        values = match.group(3).split(',')  # Assuming a simplified case for demonstration
        line_number = file_content[:match.start()].count('\n') + 1
        inserts.append((table_name, list(zip(columns, values)), line_number))

    # Debugging: Print the extracted queries
    print("Extracted Postgres UPDATE queries:", updates)
    print("Extracted Postgres INSERT queries:", inserts)

    return updates, inserts

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
            db2_updates, db2_inserts = extract_queries(db2_content)
            postgres_updates, postgres_inserts = extract_postgres_queries(postgres_content)

            # Display results in separate columns
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("DB2 UPDATE Queries")
                for i, (table_name, column_value_pairs, line_number) in enumerate(db2_updates, start=1):
                    st.write(f"Update {i} (Line {line_number}): UPDATE {table_name}")
                    st.table([{'Column': col_val.split('=')[0].strip(), 'Value': col_val.split('=')[1].strip()} for col_val in column_value_pairs.split(',')])

                st.subheader("DB2 INSERT Queries")
                for i, (table_name, column_value_pairs, line_number) in enumerate(db2_inserts, start=1):
                    st.write(f"Insert {i} (Line {line_number}): INSERT INTO {table_name}")
                    st.table([{'Column': column.strip(), 'Value': value.strip()} for column, value in column_value_pairs])

            with col2:
                st.subheader("Postgres UPDATE Queries")
                for i, (table_name, column_value_pairs, line_number) in enumerate(postgres_updates, start=1):
                    st.write(f"Update {i} (Line {line_number}): UPDATE {table_name}")
                    st.table([{'Column': col_val.split('=')[0].strip(), 'Value': col_val.split('=')[1].strip()} for col_val in column_value_pairs.split(',')])

                st.subheader("Postgres INSERT Queries")
                for i, (table_name, column_value_pairs, line_number) in enumerate(postgres_inserts, start=1):
                    st.write(f"Insert {i} (Line {line_number}): INSERT INTO {table_name}")
                    st.table([{'Column': column.strip(), 'Value': value.strip()} for column, value in column_value_pairs])
        else:
            st.error("The file names do not match. Please upload files with the same name.")

if __name__ == "__main__":
    main()
