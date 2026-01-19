import time
import os
from .checker import ping_device, check_http
from .db import init_db, log_result

import json

# Configuration
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))
TARGETS_FILE = os.path.join(os.getcwd(), 'targets.json')

def load_targets():
    try:
        with open(TARGETS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Service: Error loading targets.json: {e}")
        return []

def start_monitoring():
    print(f"Service: Initializing DB...")
    
    # Retry DB connection loop
    while True:
        try:
            init_db()
            print("Service: DB checking successful.")
            break
        except Exception as e:
            print(f"Service: DB Connection failed ({e}). Retrying in 10s...")
            time.sleep(10)

    print(f"Service: Starting monitoring loop...")
    while True:
        targets = load_targets()
        if not targets:
            print("Service: No targets found in targets.json")
        
        for target in targets:
            host = target.get('host')
            url = target.get('url')
            name = target.get('name', host)
            
            try:
                # 1. Ping Check
                ping_lat = ping_device(host)
                
                # 2. HTTP Check
                http_success, http_code, http_lat = check_http(url)
                
                # 3. Log Result
                try:
                    log_result(host, ping_lat, (http_success, http_code, http_lat))
                except Exception as db_e:
                    print(f"Service: Failed to log to DB for {name}: {db_e}")
                
                status_msg = f"[{name}] Ping: {'OK' if ping_lat else 'FAIL'}, HTTP: {'OK' if http_success else 'FAIL'}"
                print(status_msg)
                
            except Exception as e:
                print(f"Error checking {name}: {e}")
        
        time.sleep(CHECK_INTERVAL)
