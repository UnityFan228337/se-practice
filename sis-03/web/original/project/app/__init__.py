"""Smart Campus Room Availability Checker — standard-library web app.

Uses only Python's standard library (http.server) so it runs without any
pip installs. Room data and availability rules live in `rooms.py` and
`availability.py`; the page is rendered by `pages.py`; static assets are
served from `static/`.
"""
from __future__ import annotations

import json
import mimetypes
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .availability import (
    check_availability,
    label_to_minutes,
    minutes_to_label,
)
from .pages import render_index
from .rooms import ROOMS, get_room
from .serializers import campus_config, result_to_dict, room_to_dict

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


def _now_minutes() -> int:
    now = datetime.now()
    return now.hour * 60 + now.minute


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quieter console
        return

    # --- GET / ---
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            self._serve_index()
            return
        if path == "/api/check":
            self._serve_check(parsed.query)
            return
        if path.startswith("/static/"):
            self._serve_static(path[len("/static/"):])
            return

        self._send_text(HTTPStatus.NOT_FOUND, "Not found")

    # --- routes ---
    def _serve_index(self) -> None:
        now = _now_minutes()
        html = render_index(
            rooms=[room_to_dict(r) for r in ROOMS],
            config=campus_config(),
            current_minutes=now,
            current_label=minutes_to_label(now),
        )
        self._send_bytes(HTTPStatus.OK, b"text/html; charset=utf-8", html.encode())

    def _serve_check(self, query: str) -> None:
        params = parse_qs(query)
        get1 = lambda key: params.get(key, [None])[0]  # noqa: E731

        room = get_room(get1("room_id"))
        start = label_to_minutes(get1("start") or "")
        end = label_to_minutes(get1("end") or "")

        current_minutes = label_to_minutes(get1("current") or "")
        if current_minutes is None:
            current_minutes = _now_minutes()

        result = check_availability(room, start, end, current_minutes)
        payload: dict = {"result": result_to_dict(result)}
        if room is not None:
            payload["room"] = room_to_dict(room)

        body = json.dumps(payload).encode()
        self._send_bytes(HTTPStatus.OK, b"application/json", body)

    def _serve_static(self, rel: str) -> None:
        # Prevent path traversal.
        try:
            file_path = (STATIC_DIR / rel).resolve()
            file_path.relative_to(STATIC_DIR)
        except ValueError:
            self._send_text(HTTPStatus.FORBIDDEN, "Forbidden")
            return
        if not file_path.is_file():
            self._send_text(HTTPStatus.NOT_FOUND, "Not found")
            return
        ctype = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        self._send_bytes(HTTPStatus.OK, ctype.encode(), file_path.read_bytes())

    # --- low-level helpers ---
    def _send_bytes(self, status: HTTPStatus, ctype: bytes, body: bytes) -> None:
        self.send_response(int(status))
        self.send_header("Content-Type", ctype.decode())
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, status: HTTPStatus, text: str) -> None:
        self._send_bytes(status, b"text/plain; charset=utf-8", text.encode())


def create_server(port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("0.0.0.0", port), Handler)


def run(port: int = 8000) -> None:
    server = create_server(port)
    print(f"Room Availability Checker running on http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()