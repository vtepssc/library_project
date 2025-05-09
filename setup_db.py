import sqlite3

# connect to or create the database file
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# create tables
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        year INTEGER NOT NULL
    )
    ''')
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL
    )
    ''')
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS loans (
        loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        loan_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (book_id) REFERENCES books (book_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

# commit the changes and close the connection
conn.commit()
conn.close()
print("Database and tables created successfully.")