#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
import urllib.request
import json
import os

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MiningHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('directory', DIRECTORY)
        super().__init__(*args, **kwargs)

    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _blocks_file(self):
        return os.path.join(DIRECTORY, 'blocks_found.json')

    def _load_blocks(self):
        path = self._blocks_file()
        if not os.path.exists(path):
            return []
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_blocks(self, blocks):
        path = self._blocks_file()
        with open(path, 'w') as f:
            json.dump(blocks, f, indent=2, ensure_ascii=False)

    def do_GET(self):
        if self.path.startswith('/api/stats'):
            try:
                url = 'https://raw.stats.ckpool.org/users/1B2zueGu5K4NYPisus23yAejacUyp1fYyi'
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
        elif self.path == '/api/blocks':
            blocks = self._load_blocks()
            self._send_json(200, blocks)
        else:
            # Serve static files
            if self.path == '/':
                self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/api/blocks':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                new_block = json.loads(body)
                blocks = self._load_blocks()
                blocks.append(new_block)
                self._save_blocks(blocks)
                self._send_json(200, {'ok': True, 'total': len(blocks)})
            except Exception as e:
                self._send_json(400, {'error': str(e)})
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    # Ensure blocks_found.json exists
    blocks_path = os.path.join(DIRECTORY, 'blocks_found.json')
    if not os.path.exists(blocks_path):
        with open(blocks_path, 'w') as f:
            json.dump([], f)
    server = ThreadingHTTPServer(('0.0.0.0', 8080), MiningHandler)
    print('Mining dashboard running on :8080')
    server.serve_forever()
