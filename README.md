# ⛏️ ckpool Mining Dashboard

A simple, real-time mining stats dashboard for [ckpool](https://ckpool.org) solo mining pools.

![Dashboard](https://img.shields.io/badge/status-active-green) ![Python](https://img.shields.io/badge/python-3.8+-blue) ![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🇬🇧 English

### Features

- 📊 **Real-time hashrate** — 1m, 5m, 1h, 24h, 7d views
- 📈 **Charts** — hashrate comparison across all workers
- 🔧 **Per-worker stats** — click any worker to see individual details
- 🟢 **Online/offline status** — live monitoring
- 🔄 **Auto-refresh** — updates every 60 seconds
- 🔐 **No data collection** — your wallet stays in your browser (localStorage)
- 📱 **Responsive** — works on desktop and mobile

### Quick Start

```bash
# Option 1: Pass wallet as argument
python3 server.py 1YourBitcoinWalletAddress

# Option 2: Environment variable
CKPOOL_WALLET=1YourBitcoinWalletAddress python3 server.py

# Option 3: No wallet (enter in UI)
python3 server.py
```

Then open `http://localhost:8080` in your browser.

### Custom port

```bash
PORT=3000 python3 server.py 1YourBitcoinWalletAddress
```

### How it works

```
Browser ──→ server.py (proxy) ──→ raw.stats.ckpool.org API
                ↓
          serves index.html + charts
```

The Python server acts as a CORS proxy between your browser and the ckpool stats API.

### Requirements

- Python 3.8+ (no external dependencies, stdlib only)
- A Bitcoin wallet address used for ckpool solo mining

### Run as a service (systemd)

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

### Worker names

In ckpool, you can name your miners using the format:

```
WALLET.WORKERNAME
```

Example: `1A1zP1eP...NerdQaxe`

All rewards go to the wallet address. Worker names are just labels for tracking individual miners.

---

## 🇪🇸 Español

### Características

- 📊 **Hashrate en tiempo real** — vistas de 1m, 5m, 1h, 24h, 7d
- 📈 **Gráficos** — comparación de hashrate entre todos los workers
- 🔧 **Stats por worker** — haz click en un worker para ver sus detalles individuales
- 🟢 **Estado online/offline** — monitorización en vivo
- 🔄 **Auto-refresh** — se actualiza cada 60 segundos
- 🔐 **Sin recolección de datos** — tu wallet se guarda solo en tu navegador (localStorage)
- 📱 **Responsive** — funciona en escritorio y móvil

### Inicio rápido

```bash
# Opción 1: Pasar la wallet como argumento
python3 server.py 1TuWalletDeBitcoin

# Opción 2: Variable de entorno
CKPOOL_WALLET=1TuWalletDeBitcoin python3 server.py

# Opción 3: Sin wallet (introducir en la interfaz)
python3 server.py
```

Luego abre `http://localhost:8080` en tu navegador.

### Puerto personalizado

```bash
PORT=3000 python3 server.py 1TuWalletDeBitcoin
```

### Cómo funciona

```
Navegador ──→ server.py (proxy) ──→ API de raw.stats.ckpool.org
                  ↓
            sirve index.html + gráficos
```

El servidor Python actúa como proxy CORS entre tu navegador y la API de estadísticas de ckpool, ya que ckpool no envía cabeceras CORS.

### Requisitos

- Python 3.8+ (sin dependencias externas, solo stdlib)
- Una dirección de wallet de Bitcoin usada para minado solo en ckpool

### Ejecutar como servicio (systemd)

```ini
# ~/.config/systemd/user/ckpool-dashboard.service
[Unit]
Description=ckpool Mining Dashboard
After=network.target

[Service]
Type=simple
WorkingDirectory=/ruta/a/ckpool-dashboard
ExecStart=/usr/bin/python3 server.py 1TuWallet
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now ckpool-dashboard.service
```

### Nombres de workers

En ckpool puedes nombrar tus mineros usando el formato:

```
WALLET.NOMBREWORKER
```

Ejemplo: `1A1zP1eP...NerdQaxe`

Todas las recompensas van a la dirección de la wallet. Los nombres de worker son solo etiquetas para identificar cada minero en el dashboard.

---

## License / Licencia

MIT — do whatever you want / haz lo que quieras con ello.

## Contributing

PRs welcome. Keep it simple — no build tools, no npm, no frameworks. Just Python stdlib + vanilla JS + Chart.js CDN.
