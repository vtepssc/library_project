import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# insert sample users
usernames_and_passwords = [
    ("aliceUN", "password123"),
    ("bobUN", "password456"),
    ("charlieUN", "password789"),
    ("davidUN", "password101112"),
]

users = [
    ( "Alice", "Smith", "alicesmith@example.com", "123-456-7890"),
    ("Bob", "Johnson", "bobjohnson@example.com", "234-567-8901"),
    ("Charlie", "Brown", "charliebrown@example.com", "345-678-9012"),
    ("David", "Williams", "davidwilliams@example.com", "456-789-0123"),
]

for i, (username, password) in enumerate(usernames_and_passwords):
    password_hash = generate_password_hash(password)
    users[i] = (username, password_hash) + users[i]

cursor.executemany("INSERT OR IGNORE INTO users (username, password_hash, first_name, last_name, email, phone) VALUES (?, ?, ?, ?, ?, ?)", users)
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
    ("The Alchemist", "Paulo Coelho", "Adventure", 1988),
    ("The Fault in Our Stars", "John Green", "Young Adult Fiction", 2012),
    ("The Hunger Games", "Suzanne Collins", "Dystopian", 2008),
    ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 1997),
    ("The Kite Runner", "Khaled Hosseini", "Historical Fiction", 2003),
    ("The Book Thief", "Markus Zusak", "Historical Fiction", 2005),
    ("The Road", "Cormac McCarthy", "Post-Apocalyptic Fiction", 2006),
]
cursor.executemany("INSERT OR IGNORE INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)", books)

conn.commit()
conn.close()
print("Sample data populated successfully.")