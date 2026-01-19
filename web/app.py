from flask import Flask, render_template, jsonify
from monitor.db import get_recent_logs
import os

def create_app():
    app_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(app_dir, 'templates')
    
    app = Flask(__name__, template_folder=template_dir)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/status')
    @app.route('/api/status')
    def status():
        try:
            from flask import request
            host_filter = request.args.get('host')
            
            # 1. Get raw recent logs (filtered if requested)
            limit = 100
            raw_logs = get_recent_logs(limit=limit, host=host_filter)
            
            # 2. Group by Host (if we want to show all devices status even when filtered, 
            # we might need a separate query for 'latest' vs 'history'. 
            # For simplicity, if filtering, we just show history for that device).
            
            # However, the 'devices' list is for the cards. 
            # If we strictly filter logs, 'devices' might only contain the filtered host.
            # To keep cards alive, let's pull LATEST for ALL devices separately if needed, 
            # OR just accept that filtering history is the main goal.
            
            # 2. Merge Configuration with Logs
            # A. Load Configuration
            import json
            targets = []
            try:
                with open(os.path.join(app_dir.replace('web', ''), 'targets.json'), 'r') as f:
                    targets = json.load(f)
            except Exception as e:
                print(f"Web: Error loading targets.json: {e}")
            
            # Map of Host -> Status Dict
            devices_map = {}
            
            # Initialize with Config (Default "Offline" / "Pending")
            for t in targets:
                host = t.get('host')
                devices_map[host] = {
                    'host': host,
                    'status_ping': 0,
                    'status_http': 0,
                    'ping_latency': 0.0,
                    'http_latency': 0.0,
                    'http_status_code': 0,
                    'error_msg': 'No data yet',
                    'timestamp': 'Pending'
                }

            # B. Overlay Latest LOG data
            # Get latest logs for ALL devices (limit 100 to cover recent checks)
            all_latest = get_recent_logs(limit=100) 
            
            # Correct logic:
            # 1. We initialized devices_map with "Pending" status for all targets.
            # 2. We iterate through recent logs (Newest to Oldest).
            # 3. If we find a log for a host, update the map *unless* we already updated it with a newer log.
            
            # Target Hosts Set for fast lookup
            target_hosts = set(devices_map.keys())
            
            seen_logs_for_host = set()
            for log in all_latest:
                host = log['host']
                if host not in seen_logs_for_host:
                    # ONLY add if it is in our configured targets
                    if host in target_hosts:
                        devices_map[host] = log
                    seen_logs_for_host.add(host)
            
            device_list = list(devices_map.values())
            
            # B. History (Filtered)
            history = raw_logs # This is already filtered by get_recent_logs if host_filter is set
            
            return jsonify({
                'devices': device_list,  # Always show all devices in cards
                'history': history,      # Filtered history
                'db_status': 'connected'
            })
        except Exception as e:
            print(f"Web: DB Error: {e}")
            return jsonify({
                'devices': [],
                'history': [],
                'db_status': 'disconnected',
                'error': str(e)
            }), 200
        
    return app
