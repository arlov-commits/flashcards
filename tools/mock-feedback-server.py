"""A minimal PostgREST-shaped server, enough to exercise the feedback board's
remote path exactly as Supabase would serve it.

Implements only what index.html actually calls:
  GET   /feedback_public?select=*&order=created.asc
  POST  /feedback
  PATCH /feedback?id=eq.<id>&edit_token=eq.<token>
  PATCH /feedback?edit_token=eq.<token>

The read endpoint strips edit_token, mirroring the view in
feedback-schema.sql, so the test proves a reader cannot learn the secret
that would let them edit somebody else's post.
"""
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

ROWS = []
LOCK = threading.Lock()
PUBLIC_FIELDS = ['id', 'parent_id', 'kind', 'body', 'author_key',
                 'author_alias', 'author_color', 'created', 'updated', 'deleted']


def eq_filters(qs):
    """PostgREST's ?col=eq.value syntax -> {col: value}."""
    out = {}
    for k, vals in qs.items():
        if k in ('select', 'order'):
            continue
        v = vals[0]
        if v.startswith('eq.'):
            out[k] = v[3:]
    return out


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,PATCH,OPTIONS')

    def _send(self, code, payload=None):
        body = json.dumps(payload if payload is not None else []).encode()
        self.send_response(code)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == '/__count':
            return self._send(200, {'rows': len(ROWS)})
        if u.path == '/__reset':
            with LOCK:
                del ROWS[:]
            return self._send(200, {'rows': 0})
        if u.path != '/feedback_public':
            return self._send(404, {'message': 'no such relation'})
        with LOCK:
            rows = [{k: r.get(k) for k in PUBLIC_FIELDS} for r in ROWS]
        rows.sort(key=lambda r: str(r.get('created') or ''))
        self._send(200, rows)

    def do_POST(self):
        u = urlparse(self.path)
        if u.path != '/feedback':
            return self._send(404, {'message': 'no such relation'})
        n = int(self.headers.get('Content-Length') or 0)
        row = json.loads(self.rfile.read(n) or b'{}')
        body = str(row.get('body') or '')
        if not (1 <= len(body) <= 4000):
            return self._send(400, {'message': 'body length out of range'})
        if not (8 <= len(str(row.get('edit_token') or '')) <= 128):
            return self._send(400, {'message': 'edit_token length out of range'})
        with LOCK:
            ROWS.append(row)
        self._send(201, [row])

    def do_PATCH(self):
        u = urlparse(self.path)
        if u.path != '/feedback':
            return self._send(404, {'message': 'no such relation'})
        filters = eq_filters(parse_qs(u.query))
        if 'edit_token' not in filters:
            # Without the token nothing is addressable — the policy's whole point.
            return self._send(400, {'message': 'edit_token filter required'})
        n = int(self.headers.get('Content-Length') or 0)
        patch = json.loads(self.rfile.read(n) or b'{}')
        touched = []
        with LOCK:
            for r in ROWS:
                if all(str(r.get(k)) == v for k, v in filters.items()):
                    r.update(patch)
                    touched.append({k: r.get(k) for k in PUBLIC_FIELDS})
        self._send(200, touched)


if __name__ == '__main__':
    HTTPServer(('127.0.0.1', 8799), Handler).serve_forever()
