// Alice's loans

SELECT *
FROM loans l 
JOIN users u on l.user_id = u.user_id
WHERE u.name = 'Alice'