import tkinter as tk
from tkinter import ttk, messagebox
from db_connector import DBConnector
from model.movies import Movies
from model.requests import Requests
from view.display import display_movies, display_top
import configs

db_mysql = DBConnector.connect_mysql(configs.dbconfig_sakila)
movies = Movies(db_mysql.cursor)

db_sqlite = DBConnector.connect_sqlite(configs.dbname_sqlite)
requests_db = Requests(db_sqlite.cursor)

languages = [""] + movies.get_languages()
categories = [""] + movies.get_categories()

def search_movies():
    category = category_var.get() or None
    year = year_entry.get() or None
    keyword = keyword_entry.get() or None
    length = length_entry.get() or None
    language = language_var.get() or None
    actor = actor_entry.get() or None

    try:
        results = movies.get_films(
            category if category else None,
            int(year) if year else None,
            keyword if keyword else None,
            int(length) if length else None,
            language if language else None,
            actor if actor else None
        )

        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, display_movies(results))

        requests_db.save(keyword, category, year, length, language, actor)
        db_sqlite.commit()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_top_requests():
    selected_filters = [f for f, var in filter_vars.items() if var.get()]
    if not selected_filters:
        messagebox.showinfo("Info", "Please select at least one filter")
        return

    try:
        top_requests = requests_db.top(selected_filters, 5)
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, display_top(selected_filters, top_requests))
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("💖            Movie Search           💖")
root.geometry("600x900")
root.configure(bg="pink")

tk.Label(root, text="Keyword:", bg="pink").pack()
keyword_entry = tk.Entry(root, width=50)
keyword_entry.pack()

tk.Label(root, text="Category:", bg="pink").pack()
category_var = tk.StringVar()

style = ttk.Style()
style.theme_use("classic")
style.configure("TCombobox", fieldbackground="pink", background="white")

category_dropdown = ttk.Combobox(root, textvariable=category_var, values=categories, state="readonly", style="TCombobox")
category_dropdown.pack()

tk.Label(root, text="Year:", bg="pink").pack()
year_entry = tk.Entry(root, width=50)
year_entry.pack()

tk.Label(root, text="Length (min):", bg="pink").pack()
length_entry = tk.Entry(root, width=50)
length_entry.pack()

tk.Label(root, text="Language:", bg="pink").pack()
language_var = tk.StringVar()
language_dropdown = ttk.Combobox(root, textvariable=language_var, values=languages, state="readonly", style="TCombobox")
language_dropdown.pack()

tk.Label(root, text="Actor:", bg="pink").pack()
actor_entry = tk.Entry(root, width=50)
actor_entry.pack()

search_button = tk.Button(root, text="Search", command=search_movies, bg="white")
search_button.pack(pady=5)

tk.Label(root, text="Select Filters for Top Requests:", bg="pink").pack()
filter_vars = {}
filter_options = ["keyword", "category", "year", "length", "language", "actor"]
for option in filter_options:
    var = tk.BooleanVar()
    chk = tk.Checkbutton(root, text=option.capitalize(), variable=var, bg="pink")
    chk.pack(anchor="w")
    filter_vars[option] = var

top_button = tk.Button(root, text="Show top-5 requests", command=show_top_requests, bg="white")
top_button.pack(pady=5)

results_text = tk.Text(root, height=20, width=80)
results_text.pack()

root.mainloop()

db_mysql.close()
db_sqlite.close()
