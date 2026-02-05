from flask import Flask, render_template_string
import redis
import os
import socket
from datetime import datetime

app = Flask(__name__)

try:
    cache = redis.Redis(host='db', port=6379, socket_timeout=5)
except Exception as e:
    cache = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Project - Grade 4.0</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; width: 100%; text-align: center; }
        h1 { color: #1a73e8; margin-bottom: 0.5rem; }
        .status { font-weight: bold; color: #34a853; margin-bottom: 1.5rem; }
        .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left; background: #f8f9fa; padding: 1rem; border-radius: 8px; }
        .label { font-weight: bold; color: #5f6368; }
        .value { color: #202124; font-family: monospace; }
        .counter-box { margin-top: 1.5rem; padding: 1rem; background: #e8f0fe; border-radius: 8px; border: 1px solid #1a73e8; }
        .counter-value { font-size: 2rem; font-weight: bold; color: #1a73e8; }
        footer { margin-top: 1rem; font-size: 0.8rem; color: #70757a; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Projekt DevOps</h1>
        <p class="status">● System operacyjny działa poprawnie</p>
        
        <div class="info-grid">
            <div class="label">ID Kontenera:</div>
            <div class="value">{{ hostname }}</div>
            
            <div class="label">Data i czas:</div>
            <div class="value">{{ current_time }}</div>
            
            <div class="label">Baza danych:</div>
            <div class="value">Redis (Docker)</div>
        </div>

        <div class="counter-box">
            <div>Łączna liczba odwiedzin:</div>
            <div class="counter-value">{{ visits }}</div>
        </div>

        <footer>
            Nowatorski Projekt Indywidualny
        </footer>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        visits = cache.incr('counter')
    except Exception:
        visits = "Błąd bazy"

    context = {
        "visits": visits,
        "hostname": socket.gethostname(),
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return render_template_string(HTML_TEMPLATE, **context)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)