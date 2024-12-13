import sqlite3
import logging
import re

logger = logging.getLogger(__name__)

class SQLiteDAO:
    def __init__(self, db_path=':memory:'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
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
        self.conn.commit()

    def store_queries(self, queries, query_type, source):
        cursor = self.conn.cursor()
        for i, (table_name, column_value_pairs, line_number) in enumerate(queries, start=1):
            query_id = f"{query_type}_{i}"
            if isinstance(column_value_pairs, list):
                try:
                    for column, value in column_value_pairs:
                        cursor.execute('INSERT INTO query_data (id, line_number, table_name, column_name, value, source) VALUES (?, ?, ?, ?, ?, ?)',
                                       (query_id, line_number, table_name, column.strip(), value.strip() if value is not None else None, source))
                    logger.info(f"Successfully stored {query_id}")
                except sqlite3.Error as e:
                    logger.error(f"Error storing {query_id}: {e}")
        self.conn.commit()

    def fetch_all_data(self):
        cursor = self.conn.cursor()
        logger.info(f"Executing query to fetch all data: SELECT id, line_number, table_name, column_name, value, source FROM query_data")
        cursor.execute('SELECT id, line_number, table_name, column_name, value, source FROM query_data')
        return cursor.fetchall()

    def fetch_query_details(self, query_id, tbl_nm, sample_query=""):
        cursor = self.conn.cursor()
        logger.info(f"Executing query to fetch details for query_id {query_id}: SELECT id, line_number, table_name, column_name, value, source FROM query_data WHERE id = '{query_id}'")

        if query_id.startswith('select_') and sample_query:
            # Extract column names from the sample query
            match = re.search(r'SELECT\s+(.+?)\s+FROM', sample_query, re.IGNORECASE)
            if match:
                column_names = [col.strip() for col in match.group(1).split(',')]
            else:
                column_names = []
            
            placeholders = ', '.join(['?' for _ in column_names])
            
            query = f'''
                SELECT 
                    postgrescsv.pg_column_name as PGcsv,
                    db2csv.db_column_name as DB2csv,
                    CASE WHEN ?1 = '' THEN  column_names.column_name ELSE COALESCE(db2_data.column_name, postgres_data.column_name) END AS "Column Name",
                    db2_data.value as "DB2 Value",
                    postgres_data.value as "Postgres Value",
                    CASE WHEN LOWER(TRIM(db2_data.value)) = LOWER(TRIM(postgres_data.value)) THEN 'Match' ELSE 'No Match' END AS "Match"
                FROM
                (SELECT column_name, value FROM query_data WHERE id = ? AND source = "DB2") AS db2_data
                FULL OUTER JOIN
                    (SELECT column_name, value FROM query_data WHERE id = ? AND source = "Postgres") AS postgres_data
                ON LOWER(TRIM(db2_data.column_name)) = LOWER(TRIM(postgres_data.column_name))
                FULL OUTER JOIN
                    (SELECT column_name AS db_column_name FROM query_data WHERE id = 'csv' AND source = "DB2" AND table_name = ?) AS db2csv
                ON LOWER(TRIM(COALESCE(db2_data.column_name, postgres_data.column_name))) = LOWER(TRIM(db2csv.db_column_name))
                FULL OUTER JOIN
                    (SELECT column_name AS pg_column_name FROM query_data WHERE id = 'csv' AND source = "Postgres" AND table_name = LOWER(?)) AS postgrescsv
                ON LOWER(TRIM(COALESCE(db2_data.column_name, postgres_data.column_name))) = LOWER(TRIM(postgrescsv.pg_column_name))
                LEFT JOIN (SELECT value as column_name FROM (SELECT value, ROW_NUMBER() OVER () as rn FROM query_data WHERE id = 'select_columns' ) WHERE rn IN ({placeholders})) AS column_names
                ON 1=1
            '''
            
            cursor.execute(query, ["", query_id, query_id, tbl_nm, tbl_nm, *column_names])
            
        else:
            cursor.execute('''
                SELECT 
                    postgrescsv.pg_column_name as PGcsv,
                    db2csv.db_column_name as DB2csv,
                    COALESCE(db2_data.column_name, postgres_data.column_name) as "Column Name",
                    db2_data.value as "DB2 Value",
                    postgres_data.value as "Postgres Value",
                    CASE WHEN LOWER(TRIM(db2_data.value)) = LOWER(TRIM(postgres_data.value)) THEN 'Match' ELSE 'No Match' END AS "Match"
                FROM
                (SELECT column_name, value FROM query_data WHERE id = ? AND source = "DB2") AS db2_data
                FULL OUTER JOIN
                    (SELECT column_name, value FROM query_data WHERE id = ? AND source = "Postgres") AS postgres_data
                ON LOWER(TRIM(db2_data.column_name)) = LOWER(TRIM(postgres_data.column_name))
                FULL OUTER JOIN
                    (SELECT column_name AS db_column_name FROM query_data WHERE id = 'csv' AND source = "DB2" AND table_name = ?) AS db2csv
                ON LOWER(TRIM(COALESCE(db2_data.column_name, postgres_data.column_name))) = LOWER(TRIM(db2csv.db_column_name))
                FULL OUTER JOIN
                    (SELECT column_name AS pg_column_name FROM query_data WHERE id = 'csv' AND source = "Postgres" AND table_name = LOWER(?)) AS postgrescsv
                ON LOWER(TRIM(COALESCE(db2_data.column_name, postgres_data.column_name))) = LOWER(TRIM(postgrescsv.pg_column_name))
            ''', (query_id, query_id, tbl_nm, tbl_nm))
        return cursor.fetchall()

    def fetch_query_details_dx(self, query_id, tbl_nm):
        cursor = self.conn.cursor()
        logger.info(f"Executing query to fetch details for query_id {query_id} and table name {tbl_nm}")
        cursor.execute('''
            
            SELECT column_name AS pg_column_name FROM query_data WHERE id = 'csv' AND source = "Postgres" AND table_name = LOWER('GABM_CMPGN')
                           
        ''')
        return cursor.fetchall()

    def store_csv_data(self, csv_data, source='DB2'):
        cursor = self.conn.cursor()
        for tname, name, coltype, length in csv_data:
            cursor.execute('INSERT INTO query_data (id, line_number, table_name, column_name, value, source) VALUES (?, ?, ?, ?, ?, ?)',
                           ('csv', length, tname.strip(), name.strip().lower(), coltype.strip(), source))
        self.conn.commit()
        logger.info(f"CSV data successfully stored for source: {source}")

    def close(self):
        self.conn.close()
