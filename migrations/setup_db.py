import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def setup_database():
    # Database connection parameters
    db_params = {
        'dbname': os.getenv('DB_NAME', 'your_db_name'),
        'user': os.getenv('DB_USER', 'your_username'),
        'password': os.getenv('DB_PASSWORD', 'your_password'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432')
    }

    print(f"Attempting to connect to {db_params['host']}:{db_params['port']} as {db_params['user']}")  # Debug line

    # Read SQL file
    with open('001_initial_schema.sql', 'r') as file:
        sql = file.read()

    # Execute SQL
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("Database schema created successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()