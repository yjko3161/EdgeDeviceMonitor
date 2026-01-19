import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from monitor.checker import ping_device, check_http
from monitor.db import init_db, log_result, get_recent_logs

def test_backend():
    print("1. Initializing DB...")
    init_db()
    
    print("2. Testing Ping (127.0.0.1)...")
    ping_lat = ping_device("127.0.0.1")
    print(f"   Result: {ping_lat}")
    
    print("3. Testing HTTP (http://google.com for test)...")
    # Using google.com just to verifying http client works, separate from our app
    http_success, http_code, http_lat = check_http("http://google.com")
    print(f"   Result: {http_success}, {http_code}, {http_lat}")
    
    print("4. Logging Result...")
    log_result("test_host", ping_lat, (http_success, http_code, http_lat), "Test Run")
    
    print("5. Reading Log...")
    logs = get_recent_logs(1)
    if logs and logs[0]['host'] == 'test_host':
        print("   SUCCESS: Log written and retrieved.")
        print(f"   Log: {logs[0]}")
    else:
        print("   FAIL: Log not found or incorrect.")

if __name__ == "__main__":
    test_backend()
