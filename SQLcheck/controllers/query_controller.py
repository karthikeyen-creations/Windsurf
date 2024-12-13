from items.query_extractor import extract_db2_queries, extract_postgres_queries

class QueryController:
    def __init__(self, db2_content, postgres_content):
        self.db2_content = db2_content
        self.postgres_content = postgres_content

    def extract_queries(self, db2_update_pattern, db2_insert_pattern_values, db2_insert_pattern_simple):
        db2_updates, db2_inserts, db2_selects = extract_db2_queries(self.db2_content, db2_update_pattern, db2_insert_pattern_values, db2_insert_pattern_simple)
        postgres_updates, postgres_inserts, postgres_selects = extract_postgres_queries(self.postgres_content)
        return db2_updates, db2_inserts, postgres_updates, postgres_inserts, db2_selects, postgres_selects
