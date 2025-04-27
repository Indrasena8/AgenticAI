import subprocess
import threading
import socket
import webbrowser  # <--- NEW IMPORT

def get_local_ip():
    """Auto-detect your current local IP address dynamically."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def start_flask():
    subprocess.run(["python", "app.py"])

def deploy_judging_form():
    threading.Thread(target=start_flask).start()

    local_ip = get_local_ip()
    public_url = f"http://{local_ip}:5000"
    print(f"\n🔗 Direct Judge Link: {public_url}")

    # 🧠 Auto-open the judge form link in browser
    webbrowser.open(public_url)

    return public_url