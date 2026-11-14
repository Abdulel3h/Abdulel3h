#!/usr/bin/env python3
"""Build the animated terminal that opens the GitHub profile README.

    pip install fonttools brotli uharfbuzz
    python tools/build_terminal.py

Writes assets/terminal.svg (wide) and assets/terminal-mobile.svg (phones; the
README swaps it in below 600px). GitHub shows README SVGs through <img>, which
blocks scripts and every external request, so each file carries its own type:

  Geist Mono            The Geist Project Authors  embedded WOFF2 subset
  IBM Plex Sans Arabic  IBM Corp.                  Arabic name as outlines

Both fonts are SIL Open Font License 1.1. They are fetched from pinned npm
packages, checked against SHA-256 and cut down to the glyphs on screen.

Motion: one pass of about five seconds, then the frame holds. Only the last
cursor keeps blinking. With prefers-reduced-motion, or in a renderer that
ignores CSS animation, the file shows its finished frame. Output is
deterministic: two runs write byte-identical files.
"""
from __future__ import annotations

import base64
import hashlib
import io
import random
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import uharfbuzz as hb
from fontTools import subset
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(tempfile.gettempdir()) / "abdulel3h-profile-fonts"

CDN = "https://cdn.jsdelivr.net/npm/"
FONTS = {
    "mono": (
        "@fontsource/geist-mono@5.3.0/files/geist-mono-latin-400-normal.woff2",
        "3f98383b122fe015a48536cd4a1cda855a201718923ffe74931a01597107b9b5",
    ),
    "mono-light": (
        "@fontsource/geist-mono@5.3.0/files/geist-mono-latin-300-normal.woff2",
        "7fc5e1adebd264d7278a8d56e77e2e4550483fc5ad0e1013b8a47d03a59f9977",
    ),
    "arabic-light": (
        "@fontsource/ibm-plex-sans-arabic@5.3.0/files/ibm-plex-sans-arabic-arabic-300-normal.woff2",
        "441410df8013ca6c9a732c0497bb65aa6c9fc4abeb917b907a38fabe44263e2c",
    ),
}

# ── Copy. Everything the terminal says. Keep it true, keep it short. ──────────
HOST = "abdulelah@github"
NAME = "Abdulelah Alkhathami"
NAME_AR = "عبدالإله الخثعمي"
ROLE = "Applied AI Engineer · Riyadh"
FOCUS = ("AI agents", "LLM systems", "Arabic-first AI")
CMD_1 = "whoami"
CMD_2 = "cat focus"
PROMPT_COLS = 4  # "~ $ "

# ── Palette. Graphite, warm off-white, one muted sand accent. ────────────────
BG = "#0E0F11"
EDGE = "#26292E"
RULE = "#1B1E22"
DOT = "#2B2E33"
INK = "#E9E6DF"
NAME_INK = "#F4F1EB"
MUTED = "#8F9299"
FAINT = "#62676E"
SEP = "#5A5E65"
ACCENT = "#C9A86C"

MONO_STACK = 'ui-monospace,"SF Mono",Menlo,Consolas,monospace'


@dataclass(frozen=True)
class Layout:
    file: str
    width: int
    height: int
    radius: float
    bar: float            # title bar height
    dot_x: tuple
    dot_r: float
    title_size: float
    left: float
    right: float
    size: float           # terminal type size
    name_size: float
    ar_size: float
    role_size: float
    y_p1: float
    y_name: float
    y_ar: float
    y_role: float
    y_p2: float
    y_focus: tuple        # one baseline = inline list; several = one item per line
    y_p3: float
    cursor_w: float


WIDE = Layout(
    file="terminal.svg", width=880, height=356, radius=14, bar=42,
    dot_x=(24, 42, 60), dot_r=5.5, title_size=12.5, left=46, right=834,
    size=16, name_size=34, ar_size=27, role_size=16,
    y_p1=92, y_name=150, y_ar=150, y_role=182, y_p2=236, y_focus=(268,), y_p3=318,
    cursor_w=2,
)

# On phones the name spans the measure and the Arabic sits flush right beneath it.
PHONE = Layout(
    file="terminal-mobile.svg", width=390, height=446, radius=12, bar=38,
    dot_x=(20, 36, 52), dot_r=4.5, title_size=12.5, left=24, right=366,
    size=16, name_size=29, ar_size=22, role_size=15,
    y_p1=86, y_name=140, y_ar=177, y_role=211, y_p2=264, y_focus=(298, 326, 354), y_p3=408,
    cursor_w=2,
)


# ── Timeline (seconds). One main motion: the typing. ─────────────────────────
def keystrokes(text: str, start: float, rng: random.Random) -> list[float]:
    times, t = [], start
    for i in range(len(text)):
        if i:
            t += 0.072 + rng.random() * 0.058 + (0.06 if text[i - 1] == " " else 0)
        times.append(round(t, 3))
    return times


def timeline() -> dict:
    rng = random.Random(11)
    t1 = keystrokes(CMD_1, 0.6, rng)
    enter1 = t1[-1] + 0.34
    name = enter1 + 0.08
    p2 = name + 0.86
    t2 = keystrokes(CMD_2, p2 + 0.34, rng)
    enter2 = t2[-1] + 0.34
    focus = [enter2 + 0.08 + 0.13 * i for i in range(len(FOCUS))]
    return {
        "t1": t1, "enter1": enter1, "name": name, "ar": name + 0.18, "role": name + 0.34,
        "p2": p2, "t2": t2, "enter2": enter2, "focus": focus, "p3": focus[-1] + 0.52,
    }


# ── Fonts ───────────────────────────────────────────────────────────────────
def fetch(key: str) -> bytes:
    path, digest = FONTS[key]
    local = CACHE / Path(path).name
    if local.exists():
        data = local.read_bytes()
    else:
        with urllib.request.urlopen(CDN + path, timeout=30) as response:
            data = response.read()
    if hashlib.sha256(data).hexdigest() != digest:
        raise SystemExit(f"checksum mismatch for {path}")
    CACHE.mkdir(parents=True, exist_ok=True)
    local.write_bytes(data)
    return data


def embedded(key: str, text: str) -> str:
    font = TTFont(io.BytesIO(fetch(key)), recalcTimestamp=False)
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = []
    options.hinting = False
    options.desubroutinize = True
    options.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]  # keep copyright + OFL notice
    subsetter = subset.Subsetter(options)
    subsetter.populate(text="".join(sorted(set(text))))
    subsetter.subset(font)
    out = io.BytesIO()
    subset.save_font(font, out, options)
    return base64.b64encode(out.getvalue()).decode("ascii")


def num(value: float) -> str:
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def arabic_outline(text: str, size: float, right: float, baseline: float) -> str:
    """Shape the Arabic name with HarfBuzz and return it as one SVG path,
    right-aligned at `right`. Outlines sidestep bidi and font fallback."""
    font = TTFont(io.BytesIO(fetch("arabic-light")), recalcTimestamp=False)
    font.flavor = None
    raw = io.BytesIO()
    font.save(raw)
    hb_font = hb.Font(hb.Face(raw.getvalue()))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf, {"kern": True, "liga": True})
    scale = size / font["head"].unitsPerEm
    width = sum(p.x_advance for p in buf.glyph_positions) * scale
    glyphs, order = font.getGlyphSet(), font.getGlyphOrder()
    pen = SVGPathPen(glyphs, ntos=num)
    x = right - width
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        dx = x + pos.x_offset * scale
        dy = baseline - pos.y_offset * scale
        glyphs[order[info.codepoint]].draw(TransformPen(pen, (scale, 0, 0, -scale, dx, dy)))
        x += pos.x_advance * scale
    return pen.getCommands()


# ── SVG ─────────────────────────────────────────────────────────────────────
def pct(t: float, total: float) -> str:
    return num(t / total * 100) + "%"


def cursor_keyframes(name: str, frames: list[tuple[float, float, int]], total: float) -> str:
    """frames: (time, x offset, opacity). Values hold until the next frame."""
    body = "".join(
        f"{pct(t, total)}{{opacity:{o};transform:translateX({num(x)}px)}}" for t, x, o in frames
    )
    return f"@keyframes {name}{{{body}}}"


def build(L: Layout, fonts: dict) -> str:
    T = timeline()
    adv = 0.6 * L.size
    col = lambda c: L.left + c * adv  # noqa: E731
    out: list[str] = []
    add = out.append

    def delay(t: float) -> str:
        return f' style="animation-delay:{num(t)}s"'

    def prompt(y: float, at: float | None) -> None:
        anim = (' class="k"' + delay(at)) if at is not None else ""
        add(f'<g{anim}><text x="{num(col(0))}" y="{num(y)}" class="m dim">~</text>'
            f'<text x="{num(col(2))}" y="{num(y)}" class="m acc">$</text></g>')

    def typed(text: str, y: float, times: list[float]) -> None:
        for i, (ch, t) in enumerate(zip(text, times)):
            if ch != " ":
                add(f'<text x="{num(col(PROMPT_COLS + i))}" y="{num(y)}" class="m k"{delay(t)}>{ch}</text>')

    def cursor(y: float, cls: str) -> None:
        h = L.size * 1.2
        add(f'<rect class="cur {cls}" x="{num(col(PROMPT_COLS) + 1)}" y="{num(y - L.size * 0.9)}" '
            f'width="{num(L.cursor_w)}" height="{num(h)}" rx="{num(L.cursor_w / 2)}"/>')

    # Cursor travel, frame by frame.
    c1 = [(0, 0, 1)] + [(t, (i + 1) * adv, 1) for i, t in enumerate(T["t1"])] + [(T["enter1"], len(CMD_1) * adv, 0)]
    c2 = ([(0, 0, 0), (T["p2"], 0, 1)] + [(t, (i + 1) * adv, 1) for i, t in enumerate(T["t2"])]
          + [(T["enter2"], len(CMD_2) * adv, 0)])
    c1_total, c2_total = c1[-1][0], c2[-1][0]

    style = f"""
@font-face{{font-family:"T";src:url(data:font/woff2;base64,{fonts['mono']}) format("woff2")}}
@font-face{{font-family:"TL";src:url(data:font/woff2;base64,{fonts['mono-light']}) format("woff2")}}
.m{{font:{num(L.size)}px "T",{MONO_STACK};fill:{INK};font-variant-ligatures:none}}
.t{{font:{num(L.title_size)}px "T",{MONO_STACK};fill:{FAINT};letter-spacing:.02em}}
.n{{font:300 {num(L.name_size)}px "TL",{MONO_STACK};fill:{NAME_INK};letter-spacing:-.01em}}
.r{{font-size:{num(L.role_size)}px;fill:{MUTED}}}
.dim{{fill:{FAINT}}}.acc{{fill:{ACCENT}}}.sep{{fill:{SEP}}}.ar{{fill:{MUTED}}}
.cur{{fill:{ACCENT}}}.c1,.c2{{opacity:0}}
.k{{animation:k .01s linear both}}
.up{{animation:up .62s cubic-bezier(.2,.65,.25,1) both}}
.c1{{animation:c1 {num(c1_total)}s steps(1,end) both}}
.c2{{animation:c2 {num(c2_total)}s steps(1,end) both}}
.c3{{animation:k .01s linear {num(T['p3'])}s both,blink 1.15s ease-in-out {num(T['p3'] + 0.6)}s infinite}}
@keyframes k{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes up{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:none}}}}
@keyframes blink{{0%,42%{{opacity:1}}55%,88%{{opacity:0}}100%{{opacity:1}}}}
{cursor_keyframes('c1', c1, c1_total)}
{cursor_keyframes('c2', c2, c2_total)}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
""".strip()

    alt = (f"{NAME} ({NAME_AR}), {ROLE.replace(' · ', ', ')}. "
           f"Focus: {', '.join(FOCUS)}.")
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{L.width}" height="{L.height}" '
        f'viewBox="0 0 {L.width} {L.height}" role="img" aria-labelledby="title desc">')
    add(f"<title id=\"title\">{NAME} — Applied AI Engineer</title>")
    add(f'<desc id="desc">{alt}</desc>')
    add("<!-- Generated by tools/build_terminal.py. Type: Geist Mono (c) The Geist Project Authors; "
        "IBM Plex Sans Arabic (c) IBM Corp. Both SIL Open Font License 1.1. -->")
    add(f"<style>{style}</style>")

    # Window
    add(f'<rect x=".5" y=".5" width="{L.width - 1}" height="{L.height - 1}" rx="{num(L.radius)}" '
        f'fill="{BG}" stroke="{EDGE}"/>')
    for x in L.dot_x:
        add(f'<circle cx="{x}" cy="{num(L.bar / 2)}" r="{num(L.dot_r)}" fill="{DOT}"/>')
    add(f'<text x="{num(L.width / 2)}" y="{num(L.bar / 2 + L.title_size * 0.36)}" class="t" '
        f'text-anchor="middle">{HOST}</text>')
    add(f'<path d="M1 {num(L.bar + 0.5)}H{L.width - 1}" stroke="{RULE}"/>')

    # 1 · whoami
    prompt(L.y_p1, None)
    typed(CMD_1, L.y_p1, T["t1"])
    cursor(L.y_p1, "c1")
    add(f'<text x="{num(col(0) - L.name_size * 0.04)}" y="{num(L.y_name)}" class="n up"'
        f'{delay(T["name"])}>{NAME}</text>')
    add(f'<path class="ar up" d="{arabic_outline(NAME_AR, L.ar_size, L.right, L.y_ar)}"'
        f'{delay(T["ar"])}/>')
    add(f'<text x="{num(col(0))}" y="{num(L.y_role)}" class="m r up"{delay(T["role"])}>{ROLE}</text>')

    # 2 · cat focus
    prompt(L.y_p2, T["p2"])
    typed(CMD_2, L.y_p2, T["t2"])
    cursor(L.y_p2, "c2")
    if len(L.y_focus) == 1:
        c = 0
        for i, item in enumerate(FOCUS):
            sep = ""
            if i:
                sep = f'<text x="{num(col(c + 2))}" y="{num(L.y_focus[0])}" class="m sep">·</text>'
                c += 5
            add(f'<g class="up"{delay(T["focus"][i])}>{sep}'
                f'<text x="{num(col(c))}" y="{num(L.y_focus[0])}" class="m">{item}</text></g>')
            c += len(item)
    else:
        for i, (item, y) in enumerate(zip(FOCUS, L.y_focus)):
            add(f'<text x="{num(col(0))}" y="{num(y)}" class="m up"{delay(T["focus"][i])}>{item}</text>')

    # 3 · rest
    prompt(L.y_p3, T["p3"])
    cursor(L.y_p3, "c3")
    add("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    mono_text = HOST + "~$ " + CMD_1 + CMD_2 + ROLE + "".join(FOCUS) + "·"
    fonts = {"mono": embedded("mono", mono_text), "mono-light": embedded("mono-light", NAME)}
    for layout in (WIDE, PHONE):
        target = ROOT / "assets" / layout.file
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(build(layout, fonts), encoding="utf-8", newline="\n")
        print(f"wrote {target.relative_to(ROOT).as_posix()}  {target.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
