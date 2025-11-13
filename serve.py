#!/usr/bin/env python3
"""Local development server for the Space Invaders preview."""
from __future__ import annotations

import argparse
import contextlib
import http.server
import os
import socket
import threading
import webbrowser


def find_free_port(preferred: int) -> int:
    if preferred:
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(("", preferred))
            except OSError:
                pass
            else:
                return preferred
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("", 0))
        return sock.getsockname()[1]


def run_server(port: int, open_browser: bool) -> None:
    root = os.path.abspath(os.path.dirname(__file__))
    os.chdir(root)

    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.ThreadingHTTPServer(("", port), handler)

    url = f"http://localhost:{port}/index.html"
    print(f"Serving Space Invaders preview at {url}\nPress Ctrl+C to stop.")

    if open_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.server_close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the development server (default: 8000).",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not attempt to open the default web browser automatically.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    port = find_free_port(args.port)
    if port != args.port:
        print(f"Requested port {args.port} unavailable, using {port} instead.")
    run_server(port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
