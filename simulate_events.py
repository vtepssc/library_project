import sqlite3
import random
from datetime import datetime, timedelta

# decide ramdomly whether to ckeck out or return a book
def random_event():
    return random.choice(["checkout", "return"])

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

try:
    event_date = datetime.now()  # Initialize event_date
    for i in range(100):
        # Add 1 day and a random number of hours, minutes, and seconds
        event_date += timedelta(
            days=1,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        event_date_str = event_date.strftime("%Y-%m-%d %H:%M:%S")
        action = random_event()

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
            print("current available_books is:", available_books, "returning a book")
            action = "return"

        # determine which books are available for checkout
        cursor.execute("SELECT book_id FROM book_availability WHERE available = 1")

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
                (book_id, user_id, event_date_str)
            )
            print(f"Checked out Book ID: {book_id} by User ID: {user_id} on {event_date_str}")

        elif action == "return":
            # get a random unreturned loan record
            cursor.execute("SELECT loan_id, book_id, user_id, loan_date FROM loans WHERE return_date IS NULL")
            loan_records = cursor.fetchall()

            if not loan_records:
                print("No active loans to return. Skipping this event.")
                continue  # ✅ SAFETY FIX ADDED HERE

            loan_record = random.choice(loan_records)
            loan_id, book_id, user_id, loan_date = loan_record
            print(f"Returned loan id: {loan_id}, Book ID: {book_id}, User ID: {user_id}, loan date: {loan_date}")

            # return the book
            cursor.execute("UPDATE loans SET return_date = ? WHERE loan_id = ?", (event_date_str, loan_id))
            print(f"Returned Book ID: {book_id} by User ID: {user_id} on {event_date_str}")
except Exception as e:
    print(f"An error occurred: {e}")

conn.commit()
conn.close()
