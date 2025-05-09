import sqlite3

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# insert sample users
users = [
    ("Alice", "Smith", "alicesmith@example.com", "123-456-7890"),
    ("Bob", "Johnson", "bobjohnson@example.com", "234-567-8901"),
    ("Charlie", "Brown", "charliebrown@example.com", "345-678-9012"),
    ("David", "Williams", "davidwilliams@example.com", "456-789-0123"),
]

cursor.executemany("INSERT OR IGNORE INTO users (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)", users)
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print("Current users:", rows)

# insert sample books
books = [
    ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1925),
    ("To Kill a Mockingbird", "Harper Lee", "Fiction", 1960),
    ("1984", "George Orwell", "Dystopian", 1949),
    ("Moby Dick", "Herman Melville", "Adventure", 1851),
    ("War and Peace", "Leo Tolstoy", "Historical Fiction", 1869),
    ("Pride and Prejudice", "Jane Austen", "Romance", 1813),
    ("The Catcher in the Rye", "J.D. Salinger", "Fiction", 1951),
    ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937),
    ("Brave New World", "Aldous Huxley", "Dystopian", 1932),
    ("The Odyssey", "Homer", "Epic Poetry", -800),
    ("The Divine Comedy", "Dante Alighieri", "Epic Poetry", 1320),
    ("The Brothers Karamazov", "Fyodor Dostoevsky", "Philosophical Fiction", 1880),
    ("Crime and Punishment", "Fyodor Dostoevsky", "Psychological Fiction", 1866),
    ("The Picture of Dorian Gray", "Oscar Wilde", "Philosophical Fiction", 1890),

]
cursor.executemany("INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)", books)

conn.commit()
conn.close()
print("Sample data populated successfully.")