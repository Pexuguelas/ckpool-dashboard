# ⛏️ ckpool Mining Dashboard

A simple, real-time mining stats dashboard for [ckpool](https://ckpool.org) solo mining pools. 

![Dashboard](https://img.shields.io/badge/status-active-green) ![Python](https://img.shields.io/badge/python-3.8+-blue) ![License](https://img.shields.io/badge/license-MIT-blue)

## Features

- 📊 **Real-time hashrate** — 1m, 5m, 1h, 24h, 7d views
- 📈 **Charts** — hashrate comparison across all workers
- 🔧 **Per-worker stats** — click any worker to see individual details
- 🟢 **Online/offline status** — live monitoring
- 🔄 **Auto-refresh** — updates every 60 seconds
- 🔐 **No data collection** — your wallet stays in your browser (localStorage)
- 📱 **Responsive** — works on desktop and mobile

## Quick Start

### Option 1: With wallet address (recommended)

```bash
python3 server.py 1YourBitcoinWalletAddress
```

### Option 2: Environment variable

```bash
CKPOOL_WALLET=1YourBitcoinWalletAddress python3 server.py
```

### Option 3: No wallet (enter in UI)

```bash
python3 server.py
```

Then open `http://localhost:8080` in your browser and enter your wallet address.

### Custom port

```bash
PORT=3000 python3 server.py 1YourBitcoinWalletAddress
```

## How it works

```
Browser ──→ server.py (proxy) ──→ raw.stats.ckpool.org API
                ↓
          serves index.html + charts
```

The Python server acts as a CORS proxy between your browser and the ckpool stats API, since ckpool doesn't send CORS headers.

## Requirements

- Python 3.8+ (no external dependencies, uses only stdlib)
- A Bitcoin wallet address used for ckpool solo mining

## Configuration

| Method | How |
|---|---|
| CLI argument | `python3 server.py <wallet>` |
| Environment variable | `CKPOOL_WALLET=<wallet> python3 server.py` |
| Browser | Enter wallet in the UI (saved to localStorage) |
| Query param | API supports `?wallet=<address>` |

## Run as a service (systemd)

```ini
# ~/.config/systemd/user/ckpool-dashboard.service
[Unit]
Description=ckpool Mining Dashboard
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/ckpool-dashboard
ExecStart=/usr/bin/python3 server.py 1YourWalletAddress
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now ckpool-dashboard.service
```

## Worker names

In ckpool, you can name your miners using the format:

```
WALLET.WORKERNAME
```

Example: `1A1zP1eP...NerdQaxe`

All rewards go to the wallet address. Worker names are just labels for tracking individual miners in the dashboard.

## License

MIT — do whatever you want.

## Contributing

PRs welcome. Keep it simple — no build tools, no npm, no frameworks. Just Python stdlib + vanilla JS + Chart.js CDN.
