import os
import re
import secrets
import time
from flask import Flask, request, redirect, make_response, abort, render_template
from flask.wrappers import Response

try:
    import requests as _req
except ImportError:
    _req = None

app = Flask(__name__)

# ── Config ────────────────────────────────────────────────────────────────────

FLAG         = os.environ.get("FLAG", "flag{fake_flag_for_testing}")
BOT_URL      = os.environ.get("BOT_URL", "")
BOT_PASSWORD = os.environ.get("BOT_PASSWORD", secrets.token_hex(16))


# ── Data model ────────────────────────────────────────────────────────────────

def _rid(n: int = 16) -> str:
    return secrets.token_hex(n)


class User:
    def __init__(self, uid, username, password, name, rank, is_admin=False):
        self.id          = uid
        self.username    = username
        self.password    = password
        self.name        = name
        self.rank        = rank
        self.is_admin    = is_admin
        self.csrf_token  = _rid(4)


class Post:
    def __init__(self, pid, content, author_name):
        self.id          = pid
        self.content     = content
        self.author_name = author_name
        self.ts          = time.time()


_users:      dict[str, User]   = {}
_by_name:    dict[str, User]   = {}
_sessions:   dict[str, str]    = {}
_posts:      dict[str, Post]   = {}
_post_order: list[str]         = []
_rate:       dict[str, list]   = {}


def _add_user(uid, username, password, name, rank, is_admin=False) -> User:
    u = User(uid, username, password, name, rank, is_admin)
    _users[uid]        = u
    _by_name[username] = u
    return u


# Predefined crew
ADMIN = _add_user(
    "u-admin", "officer_vega", BOT_PASSWORD,
    "Častnica Vega", "Varnostna častnica", is_admin=True,
)

# Seed bulletin post
_seed = Post(
    _rid(8),
    "Vaja evakuacije zaradi sevanja je preložena na 9:00 jutri. Vsa posadka naj se javi v pristanišče 4.",
    "Stardust",
)
_posts[_seed.id] = _seed
_post_order.append(_seed.id)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _current_user() -> User | None:
    sid = request.cookies.get("sid")
    if not sid:
        return None
    uid = _sessions.get(sid)
    return _users.get(uid) if uid else None


def _rate_ok(key: str, max_n: int, window: float = 3600.0) -> bool:
    now  = time.time()
    hits = _rate[key] = [t for t in _rate.get(key, []) if now - t < window]
    if len(hits) >= max_n:
        return False
    hits.append(now)
    return True


def _summon_bot(path: str) -> None:
    if not BOT_URL:
        print(f"[bot] (no BOT_URL) would visit {path}", flush=True)
        return
    if _req is None:
        print("[bot] requests package not installed", flush=True)
        return
    try:
        _req.post(f"{BOT_URL}/visit", json={"path": path}, timeout=5)
    except Exception as e:
        print(f"[bot] summon failed: {e}", flush=True)


def _check_secret(candidate: str) -> str | None:
    return FLAG if candidate.strip() == ADMIN.csrf_token.strip() else None


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def index():
    user  = _current_user()
    posts = [_posts[pid] for pid in reversed(_post_order[-20:]) if pid in _posts]
    return render_template("index.html", user=user, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    user = _current_user()
    if user:
        return redirect("/")

    error = ""
    if request.method == "POST":
        action = request.form.get("action", "login")

        if action == "login":
            uname = request.form.get("username", "").lower().strip()
            pw    = request.form.get("password", "")
            u = _by_name.get(uname)
            if not u or u.password != pw:
                error = "Napačen klicni znak ali geslo."
            else:
                sid = _rid(24)
                _sessions[sid] = u.id
                resp = make_response(redirect("/"))
                resp.set_cookie("sid", sid, httponly=True, samesite="Lax", path="/")
                return resp

        elif action == "register":
            uname = request.form.get("username", "").lower().strip()
            pw    = request.form.get("password", "")
            name  = request.form.get("name", "").strip() or "Nov član posadke"
            if not re.match(r"^[a-z0-9_]{3,20}$", uname):
                error = "Klicni znak mora imeti 3-20 znakov: a-z 0-9 _"
            elif uname in _by_name:
                error = "Ta klicni znak je že zaseden."
            else:
                uid = "u-" + _rid(4)
                _add_user(uid, uname, pw, name, "Član posadke")
                sid = _rid(24)
                _sessions[sid] = uid
                resp = make_response(redirect("/"))
                resp.set_cookie("sid", sid, httponly=True, samesite="Lax", path="/")
                return resp

    return render_template("login.html", user=None, error=error)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    sid = request.cookies.get("sid")
    if sid:
        _sessions.pop(sid, None)
    resp = make_response(redirect("/login"))
    resp.delete_cookie("sid", path="/")
    return resp


@app.post("/post/new")
def new_post():
    user = _current_user()
    if not user:
        return redirect("/login")
    ip = request.remote_addr or "unknown"
    if not _rate_ok(f"post:{ip}", 500):
        return (
            render_template("message.html", user=user, title="Omejitev hitrosti",
                             message="Preveč objav. Upočasnite."),
            429,
        )
    content = request.form.get("content", "").strip()
    if not content:
        return redirect("/")
    p = Post(_rid(16), content, user.name)
    _posts[p.id] = p
    _post_order.append(p.id)
    if len(_post_order) > 5000:
        old = _post_order.pop(0)
        _posts.pop(old, None)
    return redirect(f"/post/{p.id}")


@app.get("/post/<post_id>")
def view_post(post_id: str):
    post = _posts.get(post_id)
    if not post:
        abort(404)
    user   = _current_user()
    secret = user.csrf_token if user else ""
    return render_template("post.html", user=user, post=post, secret=secret)


@app.post("/post/<post_id>/report")
def report_post(post_id: str):
    if post_id not in _posts:
        abort(404)
    ip = request.remote_addr or "unknown"
    if not _rate_ok(f"report:{ip}", 200):
        return Response("upočasnite", status=429)
    _summon_bot(f"/post/{post_id}")
    return Response(
        "Prijavljeno. Častnica Vega bo kmalu pregledala objavo.",
        content_type="text/plain",
    )


@app.route("/solve", methods=["GET", "POST"])
def solve():
    user     = _current_user()
    flag_val = ""
    error    = ""

    if request.method == "POST":
        ip = request.remote_addr or "unknown"
        if not _rate_ok(f"solve:{ip}", 50):
            error = "Preveč poskusov. Upočasnite."
        else:
            candidate = request.form.get("secret", "").strip()
            result    = _check_secret(candidate)
            if result:
                flag_val = result
            else:
                error = "To ni častničin varnostni žeton. Nadaljujte z uhajanjem."

    return render_template("solve.html", user=user, flag_val=flag_val, error=error)


@app.post("/admin/moderate")
def admin_moderate():
    return Response(
        "Prijava pregledana. Hvala, častnica.",
        content_type="text/plain",
    )


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
