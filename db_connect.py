import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """
    Establish a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root@123",   # update if needed
            database="art_gallery_db"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print("Failed to connect to database:", e)
        return None


def test_connection():
    """
    Tests the database connection and prints all tables.
    """
    conn = get_db_connection()
    if conn:
        print("Successfully connected to art_gallery_db")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("Tables in database:")
        for table in tables:
            print(f"  - {table[0]}")
        cursor.close()
        conn.close()
    else:
        print("Failed to connect to database")

if __name__ == "__main__":
    test_connection()
