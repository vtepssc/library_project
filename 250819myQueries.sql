SELECT 
sq1.title,
SUM(duration) AS total_duration,
COUNT(loan_id) AS total_loans

FROM (SELECT
l.loan_id,
l.book_id,
b.title,
l.loan_date,
l.return_date,
ROUND(julianday(return_date) - julianday(loan_date),2) AS duration
FROM loans l
LEFT JOIN books b ON l.book_id = b.book_id) AS sq1

GROUP BY (title)
ORDER BY total_loans DESC

