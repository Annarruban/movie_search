from collections import namedtuple


def display_movies(records: list[namedtuple]) -> str:
    if not records:
        return "No search results"

    result_str = ""
    for movie in records:
        result_str += f"""
title: {movie.title} 
category: {movie.category} 
release year: {movie.release_year} 
length: {movie.length} 
language: {movie.language} 
description: {movie.description} 
actors: {movie.actors} 

                ======================================
         """
    return result_str


def display_top(args, records: list[namedtuple]) -> str:
    args_str = ", ".join(args)
    result_str = f"Top by {args_str}:\n\n"
    for counter, record in enumerate(records, start=1):
        values = ", ".join([str(record.get(k)) for k in args])
        result_str += f"{counter}. {values}: {record['count']} times\n"
    return result_str