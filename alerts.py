import json
from pathlib import Path

FILE = Path("alerts.json")

def load_alerts():
    if not FILE.exists():
        return {}
    return json.loads(FILE.read_text())

def save_alerts(data):
    FILE.write_text(json.dumps(data, indent=2))
