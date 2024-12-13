import re
import logging
logger = logging.getLogger(__name__)

# Updated regex patterns for DB2 queries
db2_update_pattern = re.compile(r'UPDATE\s+(\w+)(?:\s+\w+)?\s+SET\s+([\s\S]+?)(?:\s+WHERE|\s*;)', re.IGNORECASE)
db2_insert_pattern_values = re.compile(r'INSERT\s+INTO\s+(\w+)(?:\s+\w+)?\s*\(([^)]+)\)\s*SELECT\s*([\s\S]+?)\s+FROM', re.IGNORECASE)
db2_insert_pattern_simple = re.compile(r'INSERT\s+INTO\s+(\w+)(?:\s+\w+)?\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\);', re.IGNORECASE)
db2_select_pattern = re.compile(r'SELECT\s+([\s\S]+?)\s+FROM\s+(\w+)(?:\s+\w+)?(?:\s+WHERE|\s*;|$)', re.IGNORECASE)


# Updated regex patterns for Postgres queries
postgres_update_pattern = re.compile(r'UPDATE\s+(\w+\.\w+)(?:\s+\w+)?(?:\s+AS\s+\w+)?\s+SET\s+([\s\S]+?)\s+WHERE', re.IGNORECASE)
postgres_insert_pattern_values = re.compile(r'INSERT\s+INTO\s+(\w+\.\w+)(?:\s+\w+)?(?:\s+AS\s+\w+)?\s*\(([^)]+)\)\s*SELECT\s*([\s\S]+?)\s+FROM', re.IGNORECASE)
postgres_insert_pattern_simple = re.compile(r'INSERT\s+INTO\s+(\w+\.\w+)(?:\s+\w+)?(?:\s+AS\s+\w+)?\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\);', re.IGNORECASE)
postgres_select_pattern = re.compile(r'SELECT\s+([\s\S]+?)\s+FROM\s+(\w+\.\w+)(?:\s+\w+)?(?:\s+WHERE|\s*;|$)', re.IGNORECASE)


# Function to extract DB2 queries
def extract_db2_queries(file_content, db2_update_pattern, db2_insert_pattern_values, db2_insert_pattern_simple):
    updates = []
    inserts = []
    selects = []

    logger.info("Extracting DB2 queries...")
    # Extract UPDATE queries
    logger.info("Extracting DB2 UPDATE queries...")
    for match in db2_update_pattern.finditer(file_content):
        logger.debug(f"Matched UPDATE statement: {match.group(0)}")
        table_name = match.group(1)
        set_clause = match.group(2)
        column_value_pairs = []
        # Use regex to split by comma that is not within parentheses
        pairs = re.split(r',\s*(?![^()]*\))', set_clause)
        for pair in pairs:
            if '=' in pair:
                column, value = pair.split('=', 1)
                # Only keep the part after the dot if alias is present
                column = column.split('.')[-1].strip()
                column_value_pairs.append((column, value.strip()))
        line_number = file_content[:match.start()].count('\n') + 1
        updates.append((table_name, column_value_pairs, line_number))
    logger.info(f"Extracted {len(updates)} UPDATE queries.")

    # Extract INSERT queries with SELECT
    logger.info("Extracting DB2 INSERT queries with SELECT...")
    for match in db2_insert_pattern_values.finditer(file_content):
        table_name = match.group(1)
        columns = [col.split('.')[-1].strip() for col in match.group(2).split(',')]
        select_clause = match.group(3)
        select_values = select_clause.split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, select_values))
        inserts.append((table_name, column_value_pairs, line_number))
    logger.info(f"Extracted {len(inserts)} INSERT queries with SELECT.")

    # Extract simple INSERT queries with VALUES
    logger.info("Extracting DB2 simple INSERT queries with VALUES...")
    for match in db2_insert_pattern_simple.finditer(file_content):
        table_name = match.group(1)
        columns = [col.split('.')[-1].strip() for col in match.group(2).split(',')]
        values = match.group(3).split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, values))
        inserts.append((table_name, column_value_pairs, line_number))
    logger.info(f"Extracted {len(inserts)} simple INSERT queries with VALUES.")

    # Extract SELECT queries
    logger.info("Extracting DB2 SELECT queries...")
    for match in db2_select_pattern.finditer(file_content):
        logger.debug(f"Matched SELECT statement: {match.group(0)}")
        select_clause = match.group(1)
        table_name = match.group(2)
        line_number = file_content[:match.start()].count('\n') + 1
        # selects.append((table_name, select_clause, line_number))
        column_value_pairs = [(col.strip(), None) for col in select_clause.split(',')]
        selects.append((table_name, column_value_pairs, line_number))
    logger.info(f"Extracted {len(selects)} SELECT queries.")


    return updates, inserts, selects

# Function to extract Postgres queries
def extract_postgres_queries(file_content):
    updates = []
    inserts = []
    selects = []

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
                # Only keep the part after the dot if alias is present
                column = column.split('.')[-1].strip()
                column_value_pairs.append((column, value.strip()))
        line_number = file_content[:match.start()].count('\n') + 1
        updates.append((table_name, column_value_pairs, line_number))

    # Extract INSERT queries with SELECT
    for match in postgres_insert_pattern_values.finditer(file_content):
        table_name = match.group(1)
        columns = [col.split('.')[-1].strip() for col in match.group(2).split(',')]
        select_clause = match.group(3)
        select_values = select_clause.split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, select_values))
        inserts.append((table_name, column_value_pairs, line_number))

    # Extract simple INSERT queries with VALUES
    for match in postgres_insert_pattern_simple.finditer(file_content):
        table_name = match.group(1)
        columns = [col.split('.')[-1].strip() for col in match.group(2).split(',')]
        values = match.group(3).split(',')
        line_number = file_content[:match.start()].count('\n') + 1
        column_value_pairs = list(zip(columns, values))
        inserts.append((table_name, column_value_pairs, line_number))

    # Extract SELECT queries
    for match in postgres_select_pattern.finditer(file_content):
        select_clause = match.group(1)
        table_name = match.group(2)
        line_number = file_content[:match.start()].count('\n') + 1
        # selects.append((table_name, select_clause, line_number))
        column_value_pairs = [(col.strip(), None) for col in select_clause.split(',')]
        selects.append((table_name, column_value_pairs, line_number))

    return updates, inserts, selects
