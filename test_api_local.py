import urllib.request
import json
import time
import sys
import threading
from app import app

def run_server():
    app.run(port=5000)

def test_api():
    # Wait for server to start
    time.sleep(2)
    
    url = "http://localhost:5000/chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer secret-demo-key"
    }
    
    # 1. First msg
    data = {"conversation_id": "test_123", "message": "You won the lottery!"}
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.load(response)
            print("Response 1:", json.dumps(result, indent=2))
    except Exception as e:
        print("Error 1:", e)

    # 2. Second msg (Reply CLAIM)
    data = {"conversation_id": "test_123", "message": "Reply CLAIM to win."}
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.load(response)
            print("Response 2:", json.dumps(result, indent=2))
    except Exception as e:
        print("Error 2:", e)

if __name__ == "__main__":
    # Run server in a thread
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    
    test_api()
