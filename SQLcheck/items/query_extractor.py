import re
import logging
logger = logging.getLogger(__name__)

# Updated regex patterns for DB2 queries
db2_update_pattern = re.compile(r'UPDATE\s+(\w+)(?:\s+\w+)?\s+SET\s+([\s\S]+?)(?:\s+WHERE|\s*;)', re.IGNORECASE)
db2_insert_pattern_values = re.compile(r'INSERT\s+INTO\s+(\w+)(?:\s+\w+)?\s*\(([^)]+)\)\s*SELECT\s*([\s\S]+?)\s+FROM', re.IGNORECASE)
db2_insert_pattern_simple = re.compile(r'INSERT\s+INTO\s+(\w+)(?:\s+\w+)?\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\);', re.IGNORECASE)
# db2_select_pattern = re.compile(r'SELECT\s+([\s\S]+?)\s+FROM\s+(\w+)(?:\s+\w+)?(?:\s+WHERE|\s*;|$)', re.IGNORECASE)
db2_select_pattern = re.compile(r'SELECT\s+([\s\S]+?)\s+FROM\s+([\s\S]+?)(?:\s+WHERE|\s*;|$)', re.IGNORECASE)
db2_parameter_pattern = re.compile(r'\b(IN|OUT)\s+(\w+)\s+(\w+\(\d+\))', re.IGNORECASE)
db2_procedure_pattern = re.compile(r'CREATE\s+PROCEDURE\s+(\w+\.\w+)\s*\(([\s\S]+?)\)\s*DYNAMIC\s+RESULT\s+SETS', re.IGNORECASE)

# Updated regex patterns for Postgres queries
postgres_update_pattern = re.compile(r'UPDATE\s+(\w+\.\w+)(?:\s+\w+)?(?:\s+AS\s+\w+)?\s+SET\s+([\s\S]+?)\s+WHERE', re.IGNORECASE)
postgres_insert_pattern_values = re.compile(r'INSERT\s+INTO\s+(\w+\.\w+)(?:\s+\w+)?(?:\s+AS\s+\w+)?\s*\(([^)]+)\)\s*SELECT\s*([\s\S]+?)\s+FROM', re.IGNORECASE)
postgres_insert_pattern_simple = re.compile(r'INSERT\s+INTO\s+(\w+\.\w+)(?:\s+\w+)?(?:\s+AS\s+\w+)?\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\);', re.IGNORECASE)
# postgres_select_pattern = re.compile(r'SELECT\s+([\s\S]+?)\s+FROM\s+(\w+\.\w+)(?:\s+\w+)?(?:\s+WHERE|\s*;|$)', re.IGNORECASE)
postgres_select_pattern = re.compile(r'SELECT\s+([\s\S]+?)\s+FROM\s+(\w+\.\w+)(?:\s+\w+)?(?:\s+AS\s+\w+)?(?:\s+JOIN\s+[\s\S]+?ON\s+[\s\S]+?|\s+WHERE|\s*;|$)', re.IGNORECASE)
postgres_parameter_pattern = re.compile(r'\b(OUT\s+)?(\w+)\s+(\w+\(\d+\))', re.IGNORECASE)
postgres_function_pattern = re.compile(r'CREATE\s+OR\s+REPLACE\s+FUNCTION\s+(\w+\.\w+)\s*\(([\s\S]+?)\)\s+RETURNS\s+RECORD', re.IGNORECASE)


# Function to extract DB2 queries
def extract_db2_queries_and_parameters(file_content):
    updates = []
    inserts = []
    selects = []
    parameters = []

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
        # print(table_name, column_value_pairs, line_number)
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

    # # Extract parameters
    # logger.info("Extracting DB2 parameters...")
    # for match in db2_parameter_pattern.finditer(file_content):
    #     # print(match)
    #     table_name = 'PARAMETERS'
    #     param_type = match.group(1)
    #     param_name = match.group(2)
    #     column_value_pairs = [(param_name, param_type)]
    #     if not parameters:
    #         line_number = file_content[:match.start()].count('\n') + 1
    #     else:
    #         line_number = parameters[0][2]
    #     # print(table_name, column_value_pairs, line_number)
    #     parameters.append((table_name, column_value_pairs, line_number))
    # logger.info(f"Extracted {len(parameters)} parameters.")

    logger.info("Extracting DB2 procedures...")
    for match in db2_procedure_pattern.finditer(file_content):
        # print(match)
        # print(match.group(2))
        logger.debug(f"Matched procedure statement: {match.group(0)}")
        table_name = 'PROCEDURES'
        parameter_lst = match.group(2)
        parameter_list = re.split(r',\s*(?![^()]*\))', parameter_lst)
        # print(parameter_list)
        column_value_pairs = []
        for param in parameter_list:
            param_type, param_name, dtype = param.split()
            # print(param_name, param_type)
            column_value_pairs.append((param_name, param_type))
        line_number = file_content[:match.start()].count('\n') + 1
        parameters.append((table_name, column_value_pairs, line_number))

    return updates, inserts, selects, parameters

# Function to extract Postgres queries
def extract_postgres_queries_and_parameters(file_content):
    updates = []
    inserts = []
    selects = []
    parameters = []

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

    # # Extract parameters
    # logger.info("Extracting Postgres parameters...")
    # for match in postgres_parameter_pattern.finditer(file_content):
    #     # print(match)
    #     table_name = 'PARAMETERS'
    #     param_name = match.group(2)
    #     param_type = match.group(1)
    #     column_value_pairs = [(param_name, param_type if param_type else 'IN')]
    #     if not parameters:
    #         line_number = file_content[:match.start()].count('\n') + 1
    #     else:
    #         line_number = parameters[0][2]
    #     # print(table_name, column_value_pairs, line_number)
    #     parameters.append((table_name, column_value_pairs, line_number))
    # logger.info(f"Extracted {len(parameters)} parameters.")

    # Extract functions
    logger.info("Extracting Postgres parameters...")
    for match in postgres_function_pattern.finditer(file_content):
        print(f"Matched function statement: {match.group(0)}")
        table_name = 'PARAMETERS'
        parameter_lst = match.group(2)
        parameter_list = re.split(r',\s*(?![^()]*\))', parameter_lst)
        print(f"parameter_list: {parameter_list}")
        column_value_pairs = []
        for param in parameter_list:
            if 'OUT ' in param:
                param_type, param_name, dtype = param.split()
                column_value_pairs.append((param_name, param_type))
            elif 'IN_' in param:
                param_name, dtype = param.split()
                param_type = 'IN'
                column_value_pairs.append((param_name, 'IN'))
        print(column_value_pairs)
        if not parameters:
            line_number = file_content[:match.start()].count('\n') + 1
        else:
            line_number = parameters[0][2]
        # print(table_name, column_value_pairs, line_number)
        parameters.append((table_name, column_value_pairs, line_number))
    logger.info(f"Extracted {len(parameters)} parameters.")

    return updates, inserts, selects, parameters

