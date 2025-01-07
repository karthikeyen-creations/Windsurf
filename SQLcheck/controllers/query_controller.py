from items.query_extractor import extract_db2_queries_and_parameters, extract_postgres_queries_and_parameters

class QueryController:
    def __init__(self, db2_content, postgres_content):
        self.db2_content = db2_content
        self.postgres_content = postgres_content

    def extract_queries_and_parameters(self,db2_update_pattern):
        db2_updates, db2_inserts, db2_selects, db2_parameters = extract_db2_queries_and_parameters(self.db2_content)
        postgres_updates, postgres_inserts, postgres_selects, postgres_parameters = extract_postgres_queries_and_parameters(self.postgres_content)

        return db2_updates, db2_inserts, postgres_updates, postgres_inserts, db2_selects, postgres_selects, db2_parameters, postgres_parameters


