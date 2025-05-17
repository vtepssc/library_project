import sqlite3
import random
from datetime import datetime, timedelta
import helpers


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

        # check how many records are in the library.db's loans table
        loan_count = cursor.execute("SELECT COUNT(*) FROM loans").fetchone()[0]
        print(f"Current number of loans: {loan_count}")

        # randomly decide whether to check out or return a book, but if loans < 5, force checkout
        if loan_count < 5:
            print("current loan_count is:", loan_count)
            action = "checkout"
        elif loan_count > 5:
            print("current loan_count is:", loan_count)
            action = helpers.random_event()



        # determine which books are available for checkout, and which are not
        
        # available book_ids
        available_book_ids = helpers.get_available_book_ids(cursor)
        print(f"Available books: {available_book_ids}")

        # unavailable book_ids == all_book_ids - available_book_ids
        all_book_ids = [row[0] for row in cursor.execute("SELECT book_id FROM books").fetchall()]
        unavailable_book_ids = list(set(all_book_ids) - set(available_book_ids))
        print(f"Unavailable books: {unavailable_book_ids}")

        if action == "checkout":
            # Randomly select a user
            cursor.execute("SELECT user_id FROM users")
            user_ids = [row[0] for row in cursor.fetchall()]
            user_id = random.choice(user_ids)

            # Select a book that is available
            book_id = random.choice(available_book_ids)

            # Insert a new loan record
            cursor.execute(
                "INSERT INTO loans (book_id, user_id, loan_date) VALUES (?, ?, ?)",
                (book_id, user_id, event_date_str)
            )
            print(f"Checked out Book ID: {book_id} by User ID: {user_id} on {event_date_str}")

        elif action == "return":
            # get a random active loan (return_date is NULL)
            loan_records = cursor.execute(
                "SELECT loan_id, book_id, user_id, loan_date FROM loans WHERE return_date IS NULL"
            ).fetchall()

            if not loan_records:
                print("No active loans to return. Skipping this event.")
                continue

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
