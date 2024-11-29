import re

# Updated regex patterns for DB2 queries
db2_update_pattern = re.compile(r'UPDATE\s+(\w+)\s+SET\s+([\s\S]+?)\s+WHERE', re.IGNORECASE)
db2_insert_pattern_values = re.compile(r'INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*SELECT\s*([\s\S]+?)\s+FROM', re.IGNORECASE)
db2_insert_pattern_simple = re.compile(r'INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\);', re.IGNORECASE)

# Updated regex patterns for Postgres queries
postgres_update_pattern = re.compile(r'UPDATE\s+(\w+\.\w+)\s+SET\s+([\s\S]+?)\s+WHERE', re.IGNORECASE)
postgres_insert_pattern_values = re.compile(r'INSERT\s+INTO\s+(\w+\.\w+)\s*\(([^)]+)\)\s*SELECT\s*([\s\S]+?)\s+FROM', re.IGNORECASE)
postgres_insert_pattern_simple = re.compile(r'INSERT\s+INTO\s+(\w+\.\w+)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\);', re.IGNORECASE)

# Function to extract DB2 queries
def extract_db2_queries(file_content):
    updates = []
    inserts = []

    # Extract UPDATE queries
    for match in db2_update_pattern.finditer(file_content):
        table_name = match.group(1)
        set_clause = match.group(2)
        column_value_pairs = []
        # Use regex to split by comma that is not within parentheses
        pairs = re.split(r',\s*(?![^()]*\))', set_clause)
        for pair in pairs:
            if '=' in pair:
                column, value = pair.split('=', 1)
                column_value_pairs.append((column.strip(), value.strip()))
        line_number = file_content[:match.start()].count('\n') + 1
        updates.append((table_name, column_value_pairs, line_number))

    # Extract INSERT queries with SELECT
    for match in db2_insert_pattern_values.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        select_clause = match.group(3)
        select_values = select_clause.split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, select_values))
        inserts.append((table_name, column_value_pairs, line_number))

    # Extract simple INSERT queries with VALUES
    for match in db2_insert_pattern_simple.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        values = match.group(3).split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, values))
        inserts.append((table_name, column_value_pairs, line_number))

    return updates, inserts

# Function to extract Postgres queries
def extract_postgres_queries(file_content):
    updates = []
    inserts = []

    # Extract UPDATE queries
    for match in postgres_update_pattern.finditer(file_content):
        table_name = match.group(1)
        set_clause = match.group(2)
        column_value_pairs = []
        # Use regex to split by comma that is not within parentheses
        pairs = re.split(r',\s*(?![^()]*\))', set_clause)
        for pair in pairs:
            if '=' in pair:
                column, value = pair.split('=', 1)
                column_value_pairs.append((column.strip(), value.strip()))
        line_number = file_content[:match.start()].count('\n') + 1
        updates.append((table_name, column_value_pairs, line_number))

    # Extract INSERT queries with SELECT
    for match in postgres_insert_pattern_values.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        select_clause = match.group(3)
        select_values = select_clause.split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, select_values))
        inserts.append((table_name, column_value_pairs, line_number))

    # Extract simple INSERT queries with VALUES
    for match in postgres_insert_pattern_simple.finditer(file_content):
        table_name = match.group(1)
        columns = match.group(2).split(',')
        values = match.group(3).split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, values))
        inserts.append((table_name, column_value_pairs, line_number))

    return updates, inserts
