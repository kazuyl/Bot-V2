from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

CURRENT_PRICE = None

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

LOG_FILE = DATA_DIR / 'webhook_log.jsonl'
TRADES_FILE = DATA_DIR / 'trades.jsonl'
POSITION_FILE = DATA_DIR / 'position.json'
STATE_FILE = DATA_DIR / 'engine_state.json'

WEBHOOK_SECRET = 'my_super_secret_key'
ACCOUNT_SIZE = 50_000
RISK_PERCENT = 0.5
POINT_VALUE = 20
MAX_CONTRACTS = 5

app = Flask(__name__)
CORS(app)

LAST_SIGNAL: dict[str, Any] | None = None
POSITION_OPEN = False
CURRENT_POSITION: dict[str, Any] | None = None

ENGINE_STATE = {
    'signals_received': 0,
    'signals_accepted': 0,
    'signals_ignored_duplicates': 0,
    'signals_ignored_position_open': 0,
    'closed_trades': 0,
    'realized_r': 0.0,
    'realized_pnl': 0.0,
}

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(payload) + '\n')

def write_json(path: Path, payload: dict[str, Any] | None) -> None:
    if payload is None:
        if path.exists():
            path.unlink()
        return
    path.write_text(json.dumps(payload, indent=2))

def read_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text())

def read_jsonl(path: Path, limit: int = 20):
    if not path.exists():
        return []
    lines = path.read_text().splitlines()
    return [json.loads(l) for l in lines[-limit:] if l.strip()]

def calculate_contracts(entry, stop):
    if entry is None or stop is None:
        return 0
    stop_distance = abs(float(entry) - float(stop))
    if stop_distance <= 0:
        return 0
    risk_amount = ACCOUNT_SIZE * (RISK_PERCENT / 100)
    per_contract = stop_distance * POINT_VALUE
    contracts = int(risk_amount / per_contract)
    return max(0, min(contracts, MAX_CONTRACTS))

def normalize_signal(data):
    return {
        'received_at': utc_now(),
        'model': data.get('model'),
        'side': data.get('side'),
        'ticker': data.get('ticker'),
        'entry': float(data.get('entry')) if data.get('entry') else None,
        'stop': float(data.get('stop')) if data.get('stop') else None,
        'tp': float(data.get('tp')) if data.get('tp') else None,
        'contracts': calculate_contracts(data.get('entry'), data.get('stop')),
        'raw': data
    }

def accept_signal(signal):
    global POSITION_OPEN, CURRENT_POSITION
    CURRENT_POSITION = {
        'status': 'open',
        'opened_at': utc_now(),
        **signal
    }
    POSITION_OPEN = True

@app.route('/')
def health():
    return 'API running', 200

@app.route('/dashboard_data')
def dashboard_data():
    trades = read_jsonl(TRADES_FILE, 50)
    return jsonify({
        'ok': True,
        'current_price': CURRENT_PRICE,
        'position_open': POSITION_OPEN,
        'current_position': CURRENT_POSITION,
        'engine_state': ENGINE_STATE,
        'metrics': {
            'closed_trades': len(trades),
            'realized_pnl': ENGINE_STATE['realized_pnl']
        },
        'recent_signals': read_jsonl(LOG_FILE, 10),
        'recent_trades': trades[-10:]
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    global CURRENT_PRICE, POSITION_OPEN

    data = request.get_json()

    if data.get('secret') != WEBHOOK_SECRET:
        return jsonify({'error': 'bad secret'}), 403

    ENGINE_STATE['signals_received'] += 1

    # 🔥 Preis setzen
    if data.get('entry'):
        CURRENT_PRICE = float(data.get('entry'))

    if POSITION_OPEN:
        return jsonify({'ok': True, 'ignored': True})

    signal = normalize_signal(data)
    append_jsonl(LOG_FILE, signal)
    accept_signal(signal)

    return jsonify({'ok': True})

@app.route('/price_update', methods=['POST'])
def price_update():
    global CURRENT_PRICE

    data = request.get_json()

    if not data or 'price' not in data:
        return jsonify({'error': 'no price'}), 400

    # 🔥 DAS WAR DER BUG FIX
    price = float(data['price'])
    CURRENT_PRICE = price

    return jsonify({
        'ok': True,
        'current_price': CURRENT_PRICE
    })

@app.route('/reset_position', methods=['POST'])
def reset():
    global POSITION_OPEN, CURRENT_POSITION
    POSITION_OPEN = False
    CURRENT_POSITION = None
    return jsonify({'ok': True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
