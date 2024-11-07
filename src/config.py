import os
# from dotenv import load_dotenv

# load_dotenv()

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'your_db_name'),
    'user': os.getenv('DB_USER', 'your_username'),
    'password': os.getenv('DB_PASSWORD', 'your_password'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'wikicrow2')