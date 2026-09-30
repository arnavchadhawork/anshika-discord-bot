from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Savage Girl Bot 24/7 Active Hai! 🔥"

def run():
    # Render, Replit, Koyeb port binding (default 8080)
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
