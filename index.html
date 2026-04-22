<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TradingView Bot Dashboard</title>
  <style>
    :root {
      --bg: #0b1020;
      --panel: #121932;
      --panel-2: #0f152b;
      --text: #edf2ff;
      --muted: #99a3c7;
      --line: rgba(255,255,255,0.08);
      --green: #2ecc71;
      --red: #ff5c5c;
      --yellow: #f5c451;
      --blue: #63a4ff;
      --shadow: 0 10px 30px rgba(0,0,0,0.25);
      --radius: 20px;
    }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: Inter, Arial, sans-serif; background: radial-gradient(circle at top, #172042 0%, var(--bg) 48%); color: var(--text); }
    .wrap { max-width: 1400px; margin: 0 auto; padding: 28px; }
    .topbar { display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap; margin-bottom:20px; }
    .card { background: linear-gradient(180deg, var(--panel), var(--panel-2)); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); padding: 20px; }
    .grid { display:grid; grid-template-columns: 1.1fr 0.9fr; gap:18px; }
    .stack { display:grid; gap:18px; }
    .row { display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; }
    .kv { background: rgba(255,255,255,0.035); border: 1px solid var(--line); border-radius: 16px; padding: 14px; }
    .kv .label { color: var(--muted); font-size: 12px; margin-bottom: 8px; }
    .kv .value { font-size: 22px; font-weight: 700; }
    .pill { padding: 10px 14px; border: 1px solid var(--line); background: rgba(255,255,255,0.04); border-radius: 999px; font-size: 13px; }
    .badge { display:inline-block; padding:8px 12px; border-radius:999px; font-size:13px; margin-right:8px; }
    .green { background: rgba(46, 204, 113, 0.12); color:#9ff0bf; }
    .red { background: rgba(255, 92, 92, 0.12); color:#ffb0b0; }
    .yellow { background: rgba(245, 196, 81, 0.12); color:#ffe4a3; }
    .list { display:grid; gap:12px; }
    .item { padding:12px; border:1px solid var(--line); border-radius:16px; background: rgba(255,255,255,0.025); }
    .muted { color: var(--muted); }
    input { width: 100%; padding: 12px; border-radius: 12px; border:1px solid var(--line); background:#0f152b; color:var(--text); }
    button { padding: 12px 16px; border-radius: 12px; border:none; cursor:pointer; }
    .actions { display:flex; gap:10px; flex-wrap:wrap; margin-top:12px; }
    @media (max-width: 1000px) { .grid, .row { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <div>
        <h1 style="margin:0">TradingView Bot Dashboard</h1>
        <p class="muted" style="margin:8px 0 0">GitHub Pages friendly dashboard for your webhook + paper-trade engine</p>
      </div>
      <div class="pill">Status: <span id="api-status">Waiting</span></div>
    </div>

    <div class="card" style="margin-bottom:18px">
      <div class="muted" style="margin-bottom:8px">API Base URL</div>
      <input id="apiBase" value="https://disown-lavender-announcer.ngrok-free.dev" />
      <div class="actions">
        <button onclick="loadData()">Refresh</button>
        <button onclick="resetPosition()">Reset Position</button>
      </div>
    </div>

    <div class="grid">
      <div class="stack">
        <div class="card">
          <h2 style="margin-top:0">Engine Metrics</h2>
          <div class="row">
            <div class="kv"><div class="label">Closed Trades</div><div class="value" id="closed_trades">-</div></div>
            <div class="kv"><div class="label">Winrate</div><div class="value" id="winrate">-</div></div>
            <div class="kv"><div class="label">Average R</div><div class="value" id="avg_r">-</div></div>
            <div class="kv"><div class="label">Realized R</div><div class="value" id="realized_r">-</div></div>
          </div>
          <div class="row" style="margin-top:12px">
            <div class="kv"><div class="label">Realized PnL</div><div class="value" id="realized_pnl">-</div></div>
            <div class="kv"><div class="label">Signals Received</div><div class="value" id="signals_received">-</div></div>
            <div class="kv"><div class="label">Signals Accepted</div><div class="value" id="signals_accepted">-</div></div>
            <div class="kv"><div class="label">Ignored</div><div class="value" id="ignored_total">-</div></div>
          </div>
        </div>

        <div class="card">
          <h2 style="margin-top:0">Open Position</h2>
          <div id="open_position_badge"></div>
          <div id="open_position" class="list"></div>
        </div>
      </div>

      <div class="stack">
        <div class="card">
          <h2 style="margin-top:0">Recent Signals</h2>
          <div id="recent_signals" class="list"></div>
        </div>
        <div class="card">
          <h2 style="margin-top:0">Recent Trades</h2>
          <div id="recent_trades" class="list"></div>
        </div>
      </div>
    </div>
  </div>

  <script>
    function fmt(v, digits = 2) {
      if (v === null || v === undefined || Number.isNaN(Number(v))) return '-';
      return Number(v).toFixed(digits);
    }
    function text(id, value) {
      const el = document.getElementById(id);
      if (el) el.textContent = value;
    }
    function apiBase() {
      return document.getElementById('apiBase').value.replace(/\/$/, '');
    }
    function itemHtml(obj) {
      return Object.entries(obj).filter(([k]) => k !== 'raw').map(([k, v]) => `<div><strong>${k}</strong>: <span class="muted">${v ?? '-'}</span></div>`).join('');
    }
    async function loadData() {
      try {
        const res = await fetch(`${apiBase()}/dashboard_data`);
        const data = await res.json();
        text('api-status', 'Connected');

        const m = data.metrics || {};
        const e = data.engine_state || {};
        text('closed_trades', m.closed_trades ?? 0);
        text('winrate', `${fmt(m.winrate)}%`);
        text('avg_r', fmt(m.avg_r, 3));
        text('realized_r', fmt(m.realized_r, 2));
        text('realized_pnl', `$${fmt(m.realized_pnl, 2)}`);
        text('signals_received', e.signals_received ?? 0);
        text('signals_accepted', e.signals_accepted ?? 0);
        text('ignored_total', (Number(e.signals_ignored_duplicates || 0) + Number(e.signals_ignored_position_open || 0)).toString());

        const openBadge = document.getElementById('open_position_badge');
        openBadge.innerHTML = data.position_open
          ? '<span class="badge green">Position Open</span>'
          : '<span class="badge yellow">No Open Position</span>';

        const open = document.getElementById('open_position');
        open.innerHTML = '';
        if (data.current_position) {
          const div = document.createElement('div');
          div.className = 'item';
          div.innerHTML = itemHtml(data.current_position);
          open.appendChild(div);
        } else {
          open.innerHTML = '<div class="muted">No active position</div>';
        }

        const sigs = document.getElementById('recent_signals');
        sigs.innerHTML = '';
        (data.recent_signals || []).forEach(s => {
          const div = document.createElement('div');
          div.className = 'item';
          div.innerHTML = itemHtml(s);
          sigs.appendChild(div);
        });
        if (!sigs.innerHTML) sigs.innerHTML = '<div class="muted">No signals yet</div>';

        const trades = document.getElementById('recent_trades');
        trades.innerHTML = '';
        (data.recent_trades || []).forEach(t => {
          const div = document.createElement('div');
          div.className = 'item';
          div.innerHTML = itemHtml(t);
          trades.appendChild(div);
        });
        if (!trades.innerHTML) trades.innerHTML = '<div class="muted">No trades yet</div>';

      } catch (err) {
        text('api-status', 'Offline');
        console.error(err);
      }
    }

    async function resetPosition() {
      await fetch(`${apiBase()}/reset_position`, { method: 'POST' });
      loadData();
    }

    loadData();
    setInterval(loadData, 5000);
  </script>
</body>
</html>
