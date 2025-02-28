# Movie Search Application

A simple movie search application with both a console and graphical user interface. The application allows users to search for movies based on various parameters and records queries in an SQLite database to display popular searches.

## Features

- **Console Interface:** Search for movies using a command-line interface.
- **Graphical Interface:** User-friendly GUI for searching movies.
- **Database Logging:** Records queries to an SQLite database.
- **Search Filters:** Find movies based on year, actor, length, and other parameters.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/movie-search-app.git
   cd movie-search-app
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Copy the configuration template and update credentials:
   ```sh
   cp configs.py.template configs.py
   ```
4. Initialize the SQLite database:
   ```sh
   sqlite3 local.db < create.sql
   ```
5. Open `configs.py` and replace the database credentials with your own.
   ```
   
6. Create a symbolic link to run the application as `movies` from anywhere:
   ```sh
   ln -s $(pwd)/run_cli.py /usr/local/bin/movie
   chmod +x /usr/local/bin/movies
   
## Usage

### Console Interface
To run the console interface:

movies

### Graphical Interface
To run the GUI:
```sh
python run_gui.py
```

## Contributing
Feel free to fork this repository and submit pull requests if you have improvements or bug fixes.
