
import sqlite3

# connect to or create the database file
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# views


# most active users
cursor.execute(
    '''
    CREATE VIEW IF NOT EXISTS most_active_users AS
    SELECT 
        u.user_id,
        u.first_name,
        u.last_name,
        COUNT(l.loan_id) AS loan_count
    FROM users u
    LEFT JOIN loans l ON u.user_id = l.user_id
    GROUP BY u.user_id
    ORDER BY loan_count DESC
    LIMIT 10
    '''
)

# most popular books
cursor.execute(
    '''
    CREATE VIEW IF NOT EXISTS most_popular_books AS
    SELECT 
        b.book_id,
        b.title,
        b.author,
        COUNT(l.loan_id) AS loan_count
    FROM books b
    LEFT JOIN loans l ON b.book_id = l.book_id
    GROUP BY b.book_id
    ORDER BY loan_count DESC
    LIMIT 10
    '''
)

# books checked out multiple times by the same users
cursor.execute(
    '''
    CREATE VIEW IF NOT EXISTS books_checked_out_multiple_times AS
    SELECT 
        b.book_id,
        b.title,
        b.author,
        u.user_id,
        u.first_name,
        u.last_name,
        COUNT(l.loan_id) AS loan_count
    FROM books b
    JOIN loans l ON b.book_id = l.book_id
    JOIN users u ON l.user_id = u.user_id
    GROUP BY b.book_id, u.user_id
    HAVING loan_count > 1
    '''
)

# a book is available if it has no loan date OR if the last return date is greater than or equal to the last loan date
cursor.execute(
    '''
    CREATE VIEW IF NOT EXISTS book_availability AS
    SELECT 
    b.book_id,
    b.title,
    b.author,
    CASE
        WHEN l.latest_loan_date IS NULL THEN 1
        WHEN l.latest_return_date >= l.latest_loan_date THEN 1
        ELSE 0
    END AS available
    FROM books b
    LEFT JOIN (
    SELECT 
        book_id,
        MAX(loan_date) AS latest_loan_date,
        MAX(return_date) AS latest_return_date
    FROM loans
    GROUP BY book_id
    ) l ON b.book_id = l.book_id
    '''
)

conn.commit()
conn.close()
print("Database and tables created successfully.")