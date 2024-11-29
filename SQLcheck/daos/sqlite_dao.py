import sqlite3
import logging

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
                                       (query_id, line_number, table_name, column.strip(), value.strip(), source))
                    logger.info(f"Successfully stored {query_id}")
                except sqlite3.Error as e:
                    logger.error(f"Error storing {query_id}: {e}")
        self.conn.commit()

    def fetch_all_data(self):
        cursor = self.conn.cursor()
        logger.info(f"Executing query to fetch all data: SELECT id, line_number, table_name, column_name, value, source FROM query_data")
        cursor.execute('SELECT id, line_number, table_name, column_name, value, source FROM query_data')
        return cursor.fetchall()

    def fetch_query_details(self, query_id, tbl_nm):
        cursor = self.conn.cursor()
        logger.info(f"Executing query to fetch details for query_id {query_id}: SELECT id, line_number, table_name, column_name, value, source FROM query_data WHERE id = '{query_id}'")
        cursor.execute('''
            SELECT 
                postgrescsv.pg_column_name as PGcsv,
                tbls1.DB2csvx as DB2csv,
                tbls1.tbls_column_name,
                tbls1.DB2_value,
                tbls1.Postgres_value,
                tbls1.value_match
            FROM
            (SELECT 
                db2csv.db_column_name AS DB2csvx,
                tbls.column_name as tbls_column_name,
                tbls.DB2_value as DB2_value,
                tbls.Postgres_value as Postgres_value,
                tbls.value_match as value_match
            FROM 
            (SELECT 
                COALESCE(LOWER(TRIM(db2.column_name)), LOWER(TRIM(postgres.column_name))) AS column_name,
                db2.value AS DB2_value,
                postgres.value AS Postgres_value,
                CASE WHEN LOWER(TRIM(db2.value)) = LOWER(TRIM(postgres.value)) THEN 'Match' ELSE 'No Match' END AS value_match
            FROM 
                (SELECT column_name, value FROM query_data WHERE id = ? AND source = "DB2") AS db2
            FULL OUTER JOIN
                (SELECT column_name, value FROM query_data WHERE id = ? AND source = "Postgres") AS postgres
            ON LOWER(TRIM(db2.column_name)) = LOWER(TRIM(postgres.column_name))) as tbls
            FULL OUTER JOIN
                (SELECT column_name AS db_column_name FROM query_data WHERE id = 'csv' AND source = "DB2" AND table_name = ?) AS db2csv
            ON LOWER(TRIM(tbls.column_name)) = LOWER(TRIM(db2csv.db_column_name))) as tbls1
            FULL OUTER JOIN
                (SELECT column_name AS pg_column_name FROM query_data WHERE id = 'csv' AND source = "Postgres" AND table_name = LOWER(?)) AS postgrescsv
            ON LOWER(TRIM(tbls1.DB2csvx)) = LOWER(TRIM(postgrescsv.pg_column_name)) 
                           
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
                           ('csv', length, tname.strip(), name.strip(), coltype.strip(), source))
        self.conn.commit()
        logger.info(f"CSV data successfully stored for source: {source}")

    def close(self):
        self.conn.close()
