#!/usr/bin/env python3
"""
ckpool Mining Dashboard - Servidor Proxy
Sirve los ficheros estáticos y hace de proxy hacia la API de ckpool.
Configura tu dirección de wallet abajo o mediante variable de entorno.
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import urllib.request
import json
import os

# === CONFIGURACIÓN ===
# Pon aquí tu dirección de wallet de Bitcoin, o usa la variable de entorno CKPOOL_WALLET
WALLET_ADDRESS = os.environ.get('CKPOOL_WALLET', 'YOUR_WALLET_ADDRESS')
# ======================

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MiningHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('directory', DIRECTORY)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path.startswith('/api/stats'):
            try:
                # Permite sobreescribir la wallet mediante query param: /api/stats?wallet=1xxx
                params = parse_qs(parsed.query)
                wallet = params.get('wallet', [WALLET_ADDRESS])[0]

                if not wallet or wallet == 'YOUR_WALLET_ADDRESS':
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'No hay wallet configurada. Usa la variable CKPOOL_WALLET o el parámetro ?wallet=.'}).encode())
                    return

                url = f'https://raw.stats.ckpool.org/users/{wallet}'
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = resp.read()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_response(502)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

        elif parsed.path == '/api/config':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'wallet': WALLET_ADDRESS if WALLET_ADDRESS != 'YOUR_WALLET_ADDRESS' else None
            }).encode())

        else:
            if parsed.path == '/':
                self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    import sys
    port = int(os.environ.get('PORT', '8080'))
    if len(sys.argv) > 1:
        WALLET_ADDRESS = sys.argv[1]

    if WALLET_ADDRESS == 'YOUR_WALLET_ADDRESS':
        print('⚠️  No hay wallet configurada!')
        print('   Uso: python3 server.py <direccion_wallet>')
        print('   O:   CKPOOL_WALLET=1xxx... python3 server.py')
        print('   O:   Cambia WALLET_ADDRESS en server.py')
        print(f'\n   El dashboard funcionará en :{port} pero debes introducir la wallet en la interfaz.')
    else:
        print(f'✅ Dashboard de minero para {WALLET_ADDRESS} funcionando en :{port}')

    server = ThreadingHTTPServer(('0.0.0.0', port), MiningHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nDeteniendo...')
        server.shutdown()
