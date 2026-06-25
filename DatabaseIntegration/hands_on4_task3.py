import mysql.connector
import time

# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="college_db"
)

cursor = conn.cursor(dictionary=True)

# ==========================================
# QUESTION 56
# Simulate the N+1 Problem
# ==========================================

print("\n===== QUESTION 56 : N+1 PROBLEM =====")

query_count = 0

start_time = time.time()

# Query 1: Fetch all enrollments
cursor.execute("SELECT * FROM enrollments")
enrollments = cursor.fetchall()
query_count += 1

results_n_plus_one = []

# N additional queries
for enrollment in enrollments:

    cursor.execute(
        """
        SELECT first_name, last_name
        FROM students
        WHERE student_id = %s
        """,
        (enrollment["student_id"],)
    )

    student = cursor.fetchone()
    query_count += 1

    results_n_plus_one.append({
        "enrollment_id": enrollment["enrollment_id"],
        "student_name": f"{student['first_name']} {student['last_name']}"
    })

end_time = time.time()

n_plus_one_time = end_time - start_time

print(f"Queries Executed: {query_count}")
print(f"Execution Time: {n_plus_one_time:.6f} seconds")

# ==========================================
# QUESTION 57
# Rewrite using a JOIN
# ==========================================

print("\n===== QUESTION 57 : JOIN SOLUTION =====")

query_count_join = 0

start_time = time.time()

cursor.execute("""
SELECT
    e.enrollment_id,
    s.first_name,
    s.last_name
FROM enrollments e
JOIN students s
ON e.student_id = s.student_id
""")

results_join = cursor.fetchall()

query_count_join += 1

end_time = time.time()

join_time = end_time - start_time

print(f"Queries Executed: {query_count_join}")
print(f"Execution Time: {join_time:.6f} seconds")

# ==========================================
# QUESTION 58
# Compare Round Trips and Timing
# ==========================================

print("\n===== QUESTION 58 : COMPARISON =====")

print(f"N+1 Queries : {query_count}")
print(f"JOIN Queries: {query_count_join}")

print(f"N+1 Time : {n_plus_one_time:.6f} sec")
print(f"JOIN Time: {join_time:.6f} sec")

print(f"Extra Queries Avoided: {query_count - query_count_join}")

# ==========================================
# QUESTION 59
# Documentation
# ==========================================

"""
QUESTION 59

For 10,000 enrollments:

N+1 Approach:
1 query to fetch enrollments
10,000 queries to fetch student names

Total Queries = 10,001

JOIN Approach:
1 query

Extra Queries Issued By N+1:
10,001 - 1 = 10,000

The JOIN approach eliminates 10,000 unnecessary
database round-trips and scales much better for
large applications.
"""

# ==========================================
# VERIFY BOTH RETURN SAME DATA
# ==========================================

print("\n===== DATA CHECK =====")

print(f"N+1 Records Returned : {len(results_n_plus_one)}")
print(f"JOIN Records Returned: {len(results_join)}")

cursor.close()
conn.close()