CREATE TABLE requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword VARCHAR(500),
    category VARCHAR(50),
    year INTEGER,
    length INTEGER,
    language VARCHAR(50),
    actor VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);





