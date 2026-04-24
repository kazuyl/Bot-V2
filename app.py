from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS

CURRENT_PRICE = None

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

LOG_FILE = DATA_DIR / "webhook_log.jsonl"
TRADES_FILE = DATA_DIR / "trades.jsonl"
POSITION_FILE = DATA_DIR / "position.json"
STATE_FILE = DATA_DIR / "engine_state.json"

WEBHOOK_SECRET = "my_super_secret_key"
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
    "signals_received": 0,
    "signals_accepted": 0,
    "signals_ignored_duplicates": 0,
    "signals_ignored_position_open": 0,
    "closed_trades": 0,
    "realized_r": 0.0,
    "realized_pnl": 0.0,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def write_json(path: Path, payload: dict[str, Any] | None) -> None:
    if payload is None:
        if path.exists():
            path.unlink()
        return
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path, limit: int = 20) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines[-limit:]:
        if line.strip():
            out.append(json.loads(line))
    return out


def calculate_contracts(entry, stop) -> int:
    if entry is None or stop is None:
        return 0

    stop_distance = abs(float(entry) - float(stop))
    if stop_distance <= 0:
        return 0

    risk_amount = ACCOUNT_SIZE * (RISK_PERCENT / 100)
    per_contract = stop_distance * POINT_VALUE
    contracts = int(risk_amount / per_contract)

    return max(0, min(contracts, MAX_CONTRACTS))


def normalize_signal(data: dict[str, Any]) -> dict[str, Any]:
    entry = data.get("entry")
    stop = data.get("stop")
    tp = data.get("tp")

    return {
        "received_at": utc_now(),
        "model": data.get("model"),
        "side": data.get("side"),
        "ticker": data.get("ticker"),
        "time": data.get("time"),
        "entry
