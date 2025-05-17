import random


def get_available_book_ids(cursor):
    cursor.execute("""
        SELECT book_id
        FROM books
        WHERE book_id NOT IN (
            SELECT book_id FROM loans WHERE return_date IS NULL
        )
    """)
    return [row[0] for row in cursor.fetchall()]

# decide ramdomly whether to ckeck out or return a book
def random_event():
    return random.choice(["checkout", "return"])