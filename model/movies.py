from collections import namedtuple


Movie = namedtuple("Movie", ["title",
    "category",
    "release_year",
    "length",
    "language",
    "description", "actors"])


class Movies:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_films(self, category, year, keyword, length, language, actor):
        args = []

        if category:
            args.append(category)

        if year:
            args.append(year)

        if keyword:
            keyword = "%" + keyword + "%"
            args.extend([keyword, keyword])

        if length:
            args.append(length)

        if language:
            args.append(language)

        if actor:
            args.append("%" + actor + "%")

        actors_aggregation = """
            GROUP_CONCAT(CONCAT(actor.first_name, ' ', actor.last_name) 
    ORDER BY actor.first_name, actor.last_name SEPARATOR ', ')
        """
        self.cursor.execute("""SELECT 
    title, 
    category.name AS category, 
    release_year, 
    length, 
    language.name AS language,
    description,""" +  actors_aggregation + """ AS actors
FROM film
INNER JOIN film_category
USING (film_id)
INNER JOIN category
USING (category_id)
INNER JOIN language
USING (language_id)
INNER JOIN film_actor
USING (film_id)
INNER JOIN actor
USING (actor_id)
WHERE TRUE
""" + (" AND category.name = %s" if category else "") +
(" AND film.release_year = %s" if year else "") +
(" AND (description LIKE %s OR title LIKE %s)" if keyword else "") +
(" AND film.length >= %s" if length else "") +
(" AND language.name = %s" if language else "") +
"""
GROUP BY film_id, title, category.name, release_year, length, language.name, description
        """ + ("HAVING " + actors_aggregation + " like %s" if actor else ""), args)
        records = self.cursor.fetchall()
        movies = [Movie(**movie) for movie in records]
        return movies

    def get_languages(self):
        self.cursor.execute("""SELECT name FROM language""")
        records = self.cursor.fetchall()
        languages = [language["name"] for language in records]
        return languages

    def get_categories(self):
        self.cursor.execute("""SELECT name FROM category""")
        records = self.cursor.fetchall()
        categories = [category["name"] for category in records]
        return categories