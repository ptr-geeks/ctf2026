# PixelBoard

A small photography forum. Anyone can read posts and comments; posting a new
message, commenting, and setting a profile picture require an account.
Self-registration is disabled — the only way to log in is the pre-seeded
`admin` account, whose password is randomly generated on every boot.

The forum also comes seeded with a handful of regular (non-admin) community
members, each with their own avatar and a couple of photography-themed
posts/comments, so it doesn't look empty on first launch.

## Project structure

```
pixelboard/
  Makefile              # build / push / run / dist / install / sync
  challenge.yml          # CTF platform metadata
  sol.py                 # reference exploit / solve script
  challenge/
    docker-compose.yml
    app/
      Dockerfile
      docker-entrypoint.sh
      src/               # PHP app (SQLite storage, no framework)
```

## Running locally

```bash
make run
```

Open http://localhost:3000. `FLAG` in `challenge/docker-compose.yml` is a
placeholder for local testing. The `admin` account's password is never
hardcoded — it's randomly generated on first boot, so nobody, including
the challenge author, knows it in advance.

## The bugs

1. **SQL injection (auth bypass) — `login.php`**
   The login query is built by concatenating `$_POST['username']` and
   `$_POST['password']` directly into a raw SQL string instead of using a
   prepared statement. Since self-registration is disabled, this is the
   intended way in.

2. **Arbitrary file upload — `profile.php`**
   The avatar upload only checks the first few bytes of the uploaded file
   against a list of known image "magic bytes" (JPEG/PNG/GIF signatures).
   It never validates the file extension, and the file is saved under its
   original name inside the public `uploads/` directory, which Apache/PHP
   will happily execute. A file that starts with a valid image header but
   is named `something.php` becomes a working webshell.

   By contrast, the image upload on `new_post.php` is properly sanitized:
   it validates the file with `getimagesize()`, picks the extension itself
   from a fixed whitelist based on the detected image type, and always
   saves it under a randomly generated filename — that upload path is not
   exploitable.

## Solving

```bash
python3 sol.py --site http://localhost:3000
```

`sol.py`:
1. Logs in as `admin` via a classic SQL injection auth-bypass payload
   (`username = admin' -- `).
2. Uploads a fake "GIF" that is actually a PHP webshell as its profile
   picture.
3. Requests the uploaded file directly to run `cat /flag.txt` and prints
   the flag.
