from db.DbQuery import DbQuery


class AdminDbQuery(DbQuery):
    def get_all_tables(self):
        return self.query("""
            SELECT sm.type as type,
                   sm.name as name,
                   sm.tbl_name as tbl_name,
                   sm.rootpage as rootpage,
                   sm.sql as sql
            FROM sqlite_master sm
            ORDER BY sm.name;
        """)

    def max_id_tours(self):
        return self.query_fetchone("""
            SELECT max(id) as max_id
            FROM tours;
        """)

    def add_tour(self, id: int, name: str):
        query = """
            INSERT INTO tours (id, name)
            VALUES (?, ?)
        """
        self.insert(
            query,
            [(id, name)]
        )

    def add_to_(self, table_name, fields):
        if table_name == "tours":
            self.add_tour(**fields)
