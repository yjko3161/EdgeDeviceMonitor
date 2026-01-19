import pymysql
import datetime
import os

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "monitor_db")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    """
    Initialize the database.
    Attempts to create the database if it doesn't exist, but suppresses errors 
    (e.g., permission denied) and proceeds to table creation assuming the DB might already exist.
    """
    # 1. Try to create local database (might fail on remote/shared hosting)
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        except Exception as e:
            print(f"DB Init: Warning - Could not create database '{DB_NAME}' (might already exist or permission denied): {e}")
        finally:
            conn.close()
    except Exception as e:
        print(f"DB Init: Warning - Could not connect to server root (check permissions): {e}")

    # 2. Create table in the specific database
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    host VARCHAR(255),
                    status_ping INT,
                    status_http INT,
                    ping_latency DOUBLE,
                    http_latency DOUBLE,
                    http_status_code INT,
                    error_msg TEXT
                )
            ''')
        conn.commit()
    finally:
        conn.close()

def log_result(host, ping_result, http_result, error_msg=None):
    """
    ping_result: float (latency) or None
    http_result: tuple (success, status_code, latency)
    """
    status_ping = 1 if ping_result is not None else 0
    ping_latency = ping_result if ping_result is not None else 0.0
    
    http_success, http_code, http_lat = http_result
    status_http = 1 if http_success else 0
    http_latency = http_lat if http_lat is not None else 0.0
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO logs (timestamp, host, status_ping, status_http, ping_latency, http_latency, http_status_code, error_msg)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (timestamp, host, status_ping, status_http, ping_latency, http_latency, http_code, error_msg))
        conn.commit()
    finally:
        conn.close()

def get_recent_logs(limit=50, host=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if host:
                cursor.execute('SELECT * FROM logs WHERE host = %s ORDER BY id DESC LIMIT %s', (host, limit))
            else:
                cursor.execute('SELECT * FROM logs ORDER BY id DESC LIMIT %s', (limit,))
            
            rows = cursor.fetchall()
            # pymysql DictCursor returns rows as dicts, but timestamp might be datetime object.
            # Convert datetime objects to string for JSON serialization consistency
            for row in rows:
                if 'timestamp' in row and isinstance(row['timestamp'], datetime.datetime):
                    row['timestamp'] = row['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        return rows
    finally:
        conn.close()
