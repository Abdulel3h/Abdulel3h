"""Signature Terminal: the design system behind every README hero on this account.

One window, one palette, one typeface, one accent, and a small set of motion
primitives. `build_terminal.py` composes the profile and project scenes from it.

Rules the primitives enforce:
- Each file is self-contained. GitHub shows README SVGs through <img>, which
  blocks scripts and external requests, so type is embedded (Geist Mono as a
  WOFF2 subset, Arabic as IBM Plex Sans Arabic outlines; both SIL OFL 1.1).
- The resting style of every element is its final state. Animations only hold
  the earlier states (`fill-mode: both`), so prefers-reduced-motion, or any
  renderer without CSS animation, shows the finished frame.
- Motion plays once. Only the last cursor keeps blinking.
- Output is deterministic: same input, byte-identical files.
"""
from __future__ import annotations

import base64
import hashlib
import io
import random
import tempfile
import urllib.request
from dataclasses import dataclass, field, replace
from functools import lru_cache
from pathlib import Path

import uharfbuzz as hb
from fontTools import subset
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

# ── Palette: graphite, warm off-white, one muted sand accent ────────────────
BG = "#0E0F11"
EDGE = "#26292E"
RULE = "#1B1E22"
DOT = "#2B2E33"
TRACK = "#1C1F23"
INK = "#E9E6DF"
NAME_INK = "#F4F1EB"
MUTED = "#8F9299"
FAINT = "#62676E"
SEP = "#5A5E65"
ACCENT = "#C9A86C"

HOST = "abdulelah@github"
MONO_STACK = 'ui-monospace,"SF Mono",Menlo,Consolas,monospace'
EASE = "cubic-bezier(.2,.65,.25,1)"

# ── Fonts: SIL OFL 1.1, pinned npm packages, verified by SHA-256 ────────────
CDN = "https://cdn.jsdelivr.net/npm/"
CACHE = Path(tempfile.gettempdir()) / "abdulel3h-profile-fonts"
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


@lru_cache(maxsize=None)
def embedded(key: str, chars: str) -> str:
    font = TTFont(io.BytesIO(fetch(key)), recalcTimestamp=False)
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = []
    options.hinting = False
    options.desubroutinize = True
    options.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]  # keep copyright + OFL notice
    subsetter = subset.Subsetter(options)
    subsetter.populate(text=chars)
    subsetter.subset(font)
    out = io.BytesIO()
    subset.save_font(font, out, options)
    return base64.b64encode(out.getvalue()).decode("ascii")


@lru_cache(maxsize=None)
def _arabic_font():
    font = TTFont(io.BytesIO(fetch("arabic-light")), recalcTimestamp=False)
    font.flavor = None
    raw = io.BytesIO()
    font.save(raw)
    return font, hb.Font(hb.Face(raw.getvalue()))


def num(value: float) -> str:
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def shape_arabic(text: str, size: float, right: float, baseline: float):
    """Shape Arabic with HarfBuzz and draw it as one path, right-aligned at `right`.
    Returns (path data, left x, cluster edges from right to left)."""
    font, hb_font = _arabic_font()
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf, {"kern": True, "liga": True})
    scale = size / font["head"].unitsPerEm
    width = sum(p.x_advance for p in buf.glyph_positions) * scale
    glyphs, order = font.getGlyphSet(), font.getGlyphOrder()
    pen = SVGPathPen(glyphs, ntos=num)
    x = right - width
    edges = []  # left edge of each glyph, visual order left→right
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        edges.append((x, info.cluster))
        glyphs[order[info.codepoint]].draw(
            TransformPen(pen, (scale, 0, 0, -scale, x + pos.x_offset * scale, baseline - pos.y_offset * scale)))
        x += pos.x_advance * scale
    # Reveal stops: one per cluster, walking right→left (reading order).
    stops, seen = [], set()
    for edge_x, cluster in reversed(edges):
        if cluster not in seen:
            seen.add(cluster)
            stops.append(edge_x)
    return pen.getCommands(), right - width, stops


def keystrokes(text: str, start: float, rng: random.Random, pace: float = 1.0) -> list[float]:
    """Human typing: a steady rhythm with small irregularities, a beat after spaces."""
    times, t = [], start
    for i in range(len(text)):
        if i:
            t += (0.072 + rng.random() * 0.058 + (0.06 if text[i - 1] == " " else 0)) * pace
        times.append(round(t, 3))
    return times


# ── Layout ──────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Layout:
    width: int
    bar: float
    left: float
    right: float
    size: float
    name_size: float
    persona_size: float
    tag_size: float
    title_size: float
    dot_x: tuple
    dot_r: float
    radius: float
    phone: bool = False


WIDE = Layout(width=880, bar=42, left=46, right=834, size=16, name_size=34, persona_size=16,
              tag_size=13, title_size=12.5, dot_x=(24, 42, 60), dot_r=5.5, radius=14)
PHONE = Layout(width=390, bar=38, left=24, right=366, size=15, name_size=29, persona_size=15,
               tag_size=12, title_size=12, dot_x=(20, 36, 52), dot_r=4.5, radius=12, phone=True)


# ── Frame: one SVG file ─────────────────────────────────────────────────────
@dataclass
class Frame:
    layout: Layout
    title: str
    desc: str
    seed: int = 11
    size: float | None = None
    body: list = field(default_factory=list)
    css: list = field(default_factory=list)
    chars: set = field(default_factory=set)
    light_chars: set = field(default_factory=set)
    cursors: int = 0

    def __post_init__(self):
        if self.size is not None:
            self.layout = replace(self.layout, size=self.size)
        self.rng = random.Random(self.seed)

    # geometry
    @property
    def L(self) -> Layout:
        return self.layout

    @property
    def adv(self) -> float:
        return 0.6 * self.L.size

    def col(self, c: float) -> float:
        return self.L.left + c * self.adv

    # low-level
    def add(self, markup: str) -> None:
        self.body.append(markup)

    def rule(self, css: str) -> None:
        self.css.append(css)

    @staticmethod
    def anim(name: str, duration: float, delay: float, timing: str = "linear", fill: str = "both") -> str:
        return f"animation:{name} {num(duration)}s {timing} {num(delay)}s {fill}"

    def window(self, start: float, end: float) -> str:
        """Visible only between `start` and `end`; hidden at rest (for passing states)."""
        return f' style="opacity:0;{self.anim("win", end - start, start, fill="none")}"'

    def appear(self, t: float) -> str:
        return f' style="{self.anim("k", .01, t)}"'

    def rise(self, t: float, duration: float = .55) -> str:
        return f' style="{self.anim("up", duration, t, EASE)}"'

    def text(self, x: float, y: float, s: str, cls: str = "m", attrs: str = "", anchor: str | None = None) -> None:
        (self.light_chars if " n" in f" {cls}" else self.chars).update(s)
        a = f' text-anchor="{anchor}"' if anchor else ""
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.add(f'<text x="{num(x)}" y="{num(y)}" class="{cls}"{a}{attrs}>{s}</text>')

    # window
    def chrome(self, height: float, path: str | None = None) -> None:
        L = self.L
        self.height = height
        self.add(f'<rect x=".5" y=".5" width="{L.width - 1}" height="{num(height - 1)}" rx="{num(L.radius)}" '
                 f'fill="{BG}" stroke="{EDGE}"/>')
        for x in L.dot_x:
            self.add(f'<circle cx="{x}" cy="{num(L.bar / 2)}" r="{num(L.dot_r)}" fill="{DOT}"/>')
        title = HOST if not (path and L.phone) else f"{HOST} {path}"
        self.text(L.width / 2, L.bar / 2 + L.title_size * .36, title, "t", anchor="middle")
        self.add(f'<path d="M1 {num(L.bar + .5)}H{L.width - 1}" stroke="{RULE}"/>')

    def header(self, name: str, persona: str, tag: str, y_name: float, y_persona: float,
               y_tag: float | None = None) -> None:
        """Project identity: name, one-line purpose, and an honest status tag."""
        L = self.L
        self.text(self.col(0) - L.name_size * .04, y_name, name, "n")
        self.text(self.col(0), y_persona, persona, "m r")
        if y_tag is None:
            self.text(L.right, y_name, tag, "m g", anchor="end")
        else:
            self.text(self.col(0), y_tag, tag, "m g")

    # prompt, typing, cursors
    def prompt(self, y: float, path: str, at: float | None = None) -> int:
        """Draw `path $` and return the column where input starts."""
        shown = "" if (self.L.phone and path != "~") else path
        attrs = self.appear(at) if at else ""
        self.add(f"<g{attrs}>")
        if shown:
            self.text(self.col(0), y, shown, "m dim")
        self.text(self.col(len(shown) + 1 if shown else 0), y, "$", "m acc")
        self.add("</g>")
        return len(shown) + 3 if shown else 2

    def cursor(self, y: float, c0: float, frames: list | None = None, rest_at: float | None = None) -> None:
        """A bar cursor. With `frames` (time, column offset, opacity) it travels with
        the typing; with `rest_at` it appears there and keeps a slow blink."""
        x = self.col(c0) + 1
        top, h = y - self.L.size * .9, self.L.size * 1.2
        if frames is not None:
            self.cursors += 1
            name, total = f"c{self.cursors}", frames[-1][0]
            body = "".join(f"{num(t / total * 100)}%{{opacity:{o};transform:translateX({num(dx * self.adv)}px)}}"
                           for t, dx, o in frames)
            self.rule(f"@keyframes {name}{{{body}}}")
            style = f"opacity:0;{self.anim(name, total, 0, 'steps(1,end)')}"
        else:
            style = f'{self.anim("k", .01, rest_at)},blink 1.15s ease-in-out {num(rest_at + .6)}s infinite'
        self.add(f'<rect class="cur" x="{num(x)}" y="{num(top)}" width="2" height="{num(h)}" rx="1" style="{style}"/>')

    def command(self, y: float, path: str, text: str, start: float, prompt_at: float = 0,
                pace: float = 1.0, wrap: str | None = None, y_wrap: float | None = None) -> float:
        """Type a command after the prompt. `wrap` continues it on a second line
        (shell-style, after a trailing backslash). Returns the time Enter lands."""
        c0 = self.prompt(y, path, prompt_at or None)
        lines = [(y, c0, text)] + ([(y_wrap, 2, wrap)] if wrap else [])
        t = start
        for i, (ly, lc, ltext) in enumerate(lines):
            times = keystrokes(ltext, t, self.rng, pace)
            for j, (ch, tt) in enumerate(zip(ltext, times)):
                if ch != " ":
                    self.text(self.col(lc + j), ly, ch, "m", self.appear(tt))
            visible_from = prompt_at if i == 0 else times[0] - .05
            frames = ([(0, 0, 0)] if visible_from > 0 else []) + [(visible_from, 0, 1)]
            frames += [(tt, j + 1, 1) for j, tt in enumerate(times)]
            end = times[-1] + (.34 if i == len(lines) - 1 else .12)
            frames.append((end, len(ltext), 0))
            self.cursor(ly, lc, frames)
            t = end + .06
        return end

    def rest(self, y: float, path: str, at: float) -> None:
        c0 = self.prompt(y, path, at)
        self.cursor(y, c0, rest_at=at)

    def arabic(self, text: str, size: float, right: float, baseline: float, cls: str, attrs: str = ""):
        d, left, stops = shape_arabic(text, size, right, baseline)
        self.add(f'<path class="{cls}" d="{d}"{attrs}/>')
        return left, stops

    # output
    def build(self) -> str:
        L = self.L
        mono = embedded("mono", "".join(sorted(self.chars | {"$"})))
        light = embedded("mono-light", "".join(sorted(self.light_chars))) if self.light_chars else None
        faces = f'@font-face{{font-family:"T";src:url(data:font/woff2;base64,{mono}) format("woff2")}}'
        if light:
            faces += f'@font-face{{font-family:"TL";src:url(data:font/woff2;base64,{light}) format("woff2")}}'
        base = f"""
{faces}
.m{{font:{num(L.size)}px "T",{MONO_STACK};fill:{INK};font-variant-ligatures:none}}
.t{{font:{num(L.title_size)}px "T",{MONO_STACK};fill:{FAINT};letter-spacing:.02em}}
.n{{font:300 {num(L.name_size)}px "TL",{MONO_STACK};fill:{NAME_INK};letter-spacing:-.01em}}
.r{{font-size:{num(L.persona_size)}px;fill:{MUTED}}}.g{{font-size:{num(L.tag_size)}px;fill:{FAINT}}}
.s{{font-size:{num(L.size * .875)}px}}
.dim{{fill:{FAINT}}}.acc{{fill:{ACCENT}}}.sep{{fill:{SEP}}}.mut{{fill:{MUTED}}}.ar{{fill:{MUTED}}}.ink{{fill:{INK}}}
.cur{{fill:{ACCENT}}}
@keyframes k{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes up{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:none}}}}
@keyframes blink{{0%,42%{{opacity:1}}55%,88%{{opacity:0}}100%{{opacity:1}}}}
@keyframes win{{from,to{{opacity:1}}}}
""".strip()
        style = "\n".join([base, *self.css, "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"])
        head = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{L.width}" height="{num(self.height)}" '
            f'viewBox="0 0 {L.width} {num(self.height)}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{self.title}</title>',
            f'<desc id="desc">{self.desc}</desc>',
            "<!-- Signature Terminal, generated by github.com/Abdulel3h/Abdulel3h tools/build_terminal.py. "
            "Type: Geist Mono (c) The Geist Project Authors; IBM Plex Sans Arabic (c) IBM Corp. "
            "Both SIL Open Font License 1.1. -->",
            f"<style>{style}</style>",
        ]
        return "\n".join(head + self.body + ["</svg>"]) + "\n"
