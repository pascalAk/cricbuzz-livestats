# utils/db_connection.py
import mysql.connector
import os

# Hardcode the .env file path - most reliable approach
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')

# Manually read .env file
def load_env():
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            port=int(os.environ.get("DB_PORT", "3306")),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", ""),
            database=os.environ.get("DB_NAME", "cricbuzz_db")
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection failed: {e}")
        return None

def close_connection(connection, cursor=None):
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    except mysql.connector.Error as e:
        print(f"Error closing connection: {e}")