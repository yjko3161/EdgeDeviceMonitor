import threading
import time
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from monitor.service import start_monitoring
from web.app import create_app

def main():
    print("Starting EdgeDeviceMonitor...")
    
    # Monitoring Service Thread
    monitor_thread = threading.Thread(target=start_monitoring, daemon=True)
    monitor_thread.start()
    
    # Web Dashboard
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
