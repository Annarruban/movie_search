class Requests:
    def __init__(self, cursor):
        self.cursor = cursor

    def save(self, keyword, category, year, length, language, actor):
        self.cursor.execute("""
        INSERT INTO requests(keyword, category, year, length, language, actor) 
        VALUES(?, ?, ?, ?, ?, ?)
        """, (keyword, category, year, length, language, actor))

    def top(self, filter_args, top_size):
        args = ",".join(filter_args)
        not_null_str = " AND ".join([f"{x} is NOT NULL" for x in filter_args])
        self.cursor.execute(f"""SELECT {args}, count(*) as count
        FROM requests 
        WHERE {not_null_str}
        GROUP BY {args}
        ORDER BY count(*)
        DESC LIMIT ?;
        """, (top_size,))
        records = self.cursor.fetchall()
        return map(dict, records)