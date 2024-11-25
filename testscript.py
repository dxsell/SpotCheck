import psycopg2

try:
    connection = psycopg2.connect(
        user="postgres",
        password="SpotCheckDB",
        host="198.58.106.46",
        port="5432",
        database="postgres"
    )
    print("Database connection successful")
    connection.close()
except Exception as e:
    print(f"Database connection failed: {e}")

