import pymysql
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

print(f"--- MariaDB Connection Diagnostic ---")
print(f"Target: {DB_HOST}:{DB_PORT}")
print(f"User:   {DB_USER}")
print(f"Pass:   {'*' * len(DB_PASSWORD) if DB_PASSWORD else '(empty)'}")

try:
    print("\nAttempting connection...")
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("SUCCESS: Connected to MariaDB server!")
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"Server Version: {version[0]}")
        
    conn.close()
    
except pymysql.err.OperationalError as e:
    code, msg = e.args
    print(f"\nFAILED: OperationalError (Code {code})")
    print(f"Message: {msg}")
    
    if code == 2003:
        print("\n[Tip] Connection Refused. Possibilities:")
        print("1. MariaDB server is NOT running.")
        print("2. MariaDB is running on a different port (check my.ini or my.cnf).")
        print("3. Firewall is blocking the connection.")
    elif code == 1045:
        print("\n[Tip] Access Denied. Possibilities:")
        print("1. Username or Password in .env is incorrect.")
        print("2. User does not have privileges to connect from localhost.")
        
except Exception as e:
    print(f"\nFAILED: {type(e).__name__}")
    print(str(e))

input("\nPress Enter to exit...")
