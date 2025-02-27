#!/usr/bin/python3


import argparse

from db_connector import DBConnector
from model.movies import Movies
from configs import dbconfig_sakila, dbname_sqlite
from view.display import display_movies, display_top
from model.requests import Requests
from utils import validate_top_args

parser = argparse.ArgumentParser(description="Movie search")

parser.add_argument("--top_size", type=int, help="Top requests size", default=5)
parser.add_argument("--top", nargs="+", help="Display top x requests")
parser.add_argument("--keyword", help="Search by keyword (e.g., --keyword=\"epic thriller\")")
parser.add_argument("--category", help="Search by movie category (e.g., --category=\"Action\")")
parser.add_argument("--year", type=int, help="Search by release year (e.g., --year=1994)")
parser.add_argument("--length", type=int, help="Search by minimal movie length in minutes (e.g., --length=120)")
parser.add_argument("--language", help="Search by language (e.g., --language=\"English\")")
parser.add_argument("--actor", help="Search by actor(s) (e.g., --actor=\"Brad Pitt, Angelina Jolie\")")
args = parser.parse_args()

cursor_sakila = DBConnector.connect_mysql(dbconfig_sakila).cursor
dbconnector_sqlite = DBConnector.connect_sqlite(dbname_sqlite)
cursor_sqlite = dbconnector_sqlite.cursor


try:
    if args.top:
        validate_top_args(args.top)
        requests = Requests(cursor_sqlite).top(args.top, args.top_size)
        print(display_top(args.top, requests))
    elif args.keyword or args.category or args.year or args.length or args.language or args.actor:
        movies = Movies(cursor_sakila)
        films = movies.get_films(
            args.category, args.year, args.keyword,
            args.length, args.language, args.actor
        )
        print(display_movies(films))
        if not films:
            languages = movies.get_languages()
            categories = movies.get_categories()
            print(f"""available languages: {", ".join(languages)}\navailable categories: {", ".join(categories)}""")
        Requests(cursor_sqlite).save(
            args.keyword, args.category, args.year,
            args.length, args.language, args.actor
        )
        dbconnector_sqlite.commit()
    else:
        print("Please specify one or more of the following:"
              " keyword, category, year, length, language or actor")
except Exception as e:
    print(e)