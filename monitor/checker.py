import requests
from ping3 import ping

def ping_device(host, timeout=2):
    """
    Pings the host.
    Returns:
        float: Latency in seconds if successful.
        None: If ping fails.
    """
    try:
        # ping3.ping returns seconds or None/False on timeout/error
        result = ping(host, timeout=timeout)
        if result is None or result is False:
            return None
        return result
    except Exception as e:
        print(f"Ping error for {host}: {e}")
        return None

def check_http(url, timeout=5):
    """
    Checks HTTP status of the URL.
    Returns:
        tuple: (success: bool, status_code: int/None, latency: float/None)
    """
    try:
        response = requests.get(url, timeout=timeout)
        return True, response.status_code, response.elapsed.total_seconds()
    except requests.RequestException as e:
        print(f"HTTP error for {url}: {e}")
        return False, None, None
