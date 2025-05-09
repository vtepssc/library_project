import sqlite3
import random
from datetime import datetime, timedelta

# decide ramdomly whether to ckeck out or return a book
def random_event():
    return random.choice(["checkout", "return"])

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

for _ in range(100):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    action = random_event()
    print(f"Action: {action}")

    # check how many records are in the library.db's loans table
    loan_count = cursor.execute("SELECT COUNT(*) FROM loans").fetchone()[0]
    print(f"Current number of loans: {loan_count}")

    # if the number of loans is less than 5, check out a book
    if loan_count < 5:
        print("current loan_count is:", loan_count)
        action = "checkout"
    elif loan_count > 5:
        print("current loan_count is:", loan_count)

    # if 5 books or less are available, return a book
    available_books = cursor.execute("SELECT COUNT(*) FROM book_availability WHERE available = 1").fetchone()[0]
    print(f"Available books: {available_books}")
    if available_books <= 5:
        print("current available_books is:", available_books ,"returning a book")
        action = "return"

    # determine which books are available for checkout
    cursor.execute("SELECT book_id FROM book_availability WHERE available = true")
                
    if action == "checkout":
        # Randomly select a user
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        user_id = random.choice(user_ids)

        # Select a book that is available
        cursor.execute("SELECT book_id FROM book_availability WHERE available = 1")
        book_ids = [row[0] for row in cursor.fetchall()]
        book_id = random.choice(book_ids)

        # Insert a new loan record
        cursor.execute(
            "INSERT INTO loans (book_id, user_id, loan_date) VALUES (?, ?, ?)",
            (book_id, user_id, now)
        )
        print(f"Checked out Book ID: {book_id} by User ID: {user_id} on {now}")

    elif action == "return":
        # get a random unreturned loan record 
        cursor.execute("SELECT loan_id, book_id, user_id, loan_date FROM loans WHERE return_date IS NULL")
        loan_records = cursor.fetchall()
        loan_record = random.choice(loan_records)
        loan_id, book_id, user_id, loan_date = loan_record
        print(f"Returned loan id: {loan_id}, Book ID: {book_id}, User ID: {user_id}, loan date: {loan_date}")

        # return the book
        cursor.execute("UPDATE loans SET return_date = ? WHERE loan_id = ?", (now, loan_id))
        print(f"Returned Book ID: {book_id} by User ID: {user_id} on {now}")

        


conn.commit()
conn.close()