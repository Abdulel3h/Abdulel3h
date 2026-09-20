#!/usr/bin/env python3
"""Generate the sculptural retro-futuristic SVG identity used by the profile README.

One material language drives every asset: inflated tubular geometry, frosted
translucent surfaces, a cyan-aqua-lime-blue gradient family, cinematic key light
from the upper left, soft contact shadows and a fine analog grain.

The generator is dependency-free and deterministic - running it twice produces
byte-identical files. Never hand-edit the generated SVGs; edit this file and
regenerate with:

    python3 tools/build_retro_future_profile.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# --------------------------------------------------------------------------
# Design tokens
# --------------------------------------------------------------------------

BLACK = "#030706"
SURFACE = "#06100E"
BORDER = "#123029"
WHITE = "#F4FFF9"
MUTED = "#8FA8A1"
DIM = "#5E7A74"
CYAN = "#46F6FF"
AQUA = "#22E3C5"
LIME = "#C8FF54"
BLUE = "#3B65FF"

SANS = 'ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, "SF Mono", "Cascadia Mono", "Segoe UI Mono", Consolas, monospace'

# Key light: upper left, cinematic.
AZIMUTH = 228
ELEVATION = 58


# --------------------------------------------------------------------------
# Material system
# --------------------------------------------------------------------------

def _gloss(name: str, bump: float, exponent: int, constant: float, rim: float) -> str:
    """A lighting filter that inflates flat geometry into a glossy translucent solid.

    The blurred alpha channel acts as a height field, so any silhouette gains a
    soft bevel, diffuse shading, a cyan rim on the shadow side and a controlled
    specular highlight.
    """
    return f"""
    <filter id="{name}" x="-35%" y="-35%" width="170%" height="170%" color-interpolation-filters="sRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="{bump}" result="bump"/>
      <feDiffuseLighting in="bump" surfaceScale="{bump * .5:.2f}" diffuseConstant="1.15" lighting-color="#CFEFFF" result="dif">
        <feDistantLight azimuth="{AZIMUTH}" elevation="{ELEVATION - 10}"/>
      </feDiffuseLighting>
      <feComposite in="dif" in2="SourceAlpha" operator="in" result="difc"/>
      <feBlend in="SourceGraphic" in2="difc" mode="multiply" result="mul"/>
      <feComposite in="mul" in2="SourceGraphic" operator="arithmetic" k2=".72" k3=".38" result="shaded"/>
      <feOffset in="SourceAlpha" dx="{rim:.1f}" dy="{rim * 1.1:.1f}" result="ro"/>
      <feComposite in="SourceAlpha" in2="ro" operator="out" result="rmask"/>
      <feGaussianBlur in="rmask" stdDeviation="{rim * .55:.2f}" result="rsoft"/>
      <feFlood flood-color="{CYAN}" flood-opacity=".9" result="rcol"/>
      <feComposite in="rcol" in2="rsoft" operator="in" result="rim0"/>
      <feComposite in="rim0" in2="SourceAlpha" operator="in" result="rim"/>
      <feComposite in="rim" in2="shaded" operator="arithmetic" k2=".72" k3="1" result="base"/>
      <feSpecularLighting in="bump" surfaceScale="{bump * .75:.2f}" specularConstant="{constant}" specularExponent="{exponent}" lighting-color="#EAFEFF" result="spec">
        <feDistantLight azimuth="{AZIMUTH}" elevation="{ELEVATION}"/>
      </feSpecularLighting>
      <feComposite in="spec" in2="SourceAlpha" operator="in" result="specc"/>
      <feComposite in="specc" in2="base" operator="arithmetic" k2="1" k3="1"/>
    </filter>"""


def defs() -> str:
    """Gradients, filters and clip geometry shared by every asset."""
    return f"""  <defs>
    <linearGradient id="glass" x1="0" y1="0" x2=".85" y2="1">
      <stop stop-color="{CYAN}"/><stop offset=".40" stop-color="{AQUA}"/>
      <stop offset=".76" stop-color="{LIME}"/><stop offset="1" stop-color="{BLUE}"/>
    </linearGradient>
    <linearGradient id="glassBack" x1="1" y1="0" x2="0" y2="1">
      <stop stop-color="{AQUA}"/><stop offset=".55" stop-color="{BLUE}"/>
      <stop offset="1" stop-color="#1B3E8F"/>
    </linearGradient>
    <linearGradient id="glassLime" x1="0" y1="1" x2="1" y2="0">
      <stop stop-color="{AQUA}"/><stop offset=".55" stop-color="{LIME}"/>
      <stop offset="1" stop-color="#EFFFC9"/>
    </linearGradient>
    <linearGradient id="glassCold" x1="0" y1="0" x2=".6" y2="1">
      <stop stop-color="#E8FBFF"/><stop offset=".45" stop-color="{CYAN}" stop-opacity=".92"/>
      <stop offset="1" stop-color="{BLUE}"/>
    </linearGradient>
    <linearGradient id="inkFade" x1="0" y1="0" x2="1" y2="0">
      <stop stop-color="{WHITE}"/><stop offset=".62" stop-color="{AQUA}"/><stop offset="1" stop-color="{CYAN}"/>
    </linearGradient>
    <linearGradient id="hair" x1="0" y1="0" x2="1" y2="0">
      <stop stop-color="{AQUA}" stop-opacity=".55"/><stop offset="1" stop-color="{AQUA}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ribbon" x1="0" y1="0" x2="1" y2="0">
      <stop stop-color="{AQUA}" stop-opacity="0"/><stop offset=".3" stop-color="{AQUA}" stop-opacity=".8"/>
      <stop offset=".7" stop-color="{LIME}"/><stop offset="1" stop-color="{CYAN}"/>
    </linearGradient>
    <radialGradient id="core" cx="36%" cy="30%" r="70%">
      <stop stop-color="#FFFFFF"/><stop offset=".18" stop-color="{CYAN}"/>
      <stop offset=".58" stop-color="{AQUA}"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".9"/>
    </radialGradient>
    <radialGradient id="coreLime" cx="36%" cy="30%" r="70%">
      <stop stop-color="#FFFFFF"/><stop offset=".2" stop-color="{LIME}"/>
      <stop offset=".62" stop-color="{AQUA}"/><stop offset="1" stop-color="#17705F"/>
    </radialGradient>
    <radialGradient id="haze">
      <stop stop-color="{AQUA}" stop-opacity=".26"/><stop offset=".55" stop-color="{AQUA}" stop-opacity=".08"/>
      <stop offset="1" stop-color="{AQUA}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="hazeLime">
      <stop stop-color="{LIME}" stop-opacity=".30"/><stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vignette" cx="50%" cy="42%" r="78%">
      <stop stop-color="{SURFACE}"/><stop offset=".55" stop-color="#040B09"/><stop offset="1" stop-color="{BLACK}"/>
    </radialGradient>
    <radialGradient id="pool" cx="50%" cy="50%" r="50%">
      <stop stop-color="#0E4B43" stop-opacity=".85"/><stop offset="1" stop-color="#0E4B43" stop-opacity="0"/>
    </radialGradient>
{_gloss('glossL', 15, 26, .82, 7)}
{_gloss('glossM', 10, 34, .90, 5)}
{_gloss('glossS', 6, 44, 1.00, 3)}
    <filter id="shade" x="-70%" y="-140%" width="240%" height="380%"><feGaussianBlur stdDeviation="20"/></filter>
    <filter id="bloom" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
    <filter id="bloomS" x="-90%" y="-90%" width="280%" height="280%"><feGaussianBlur stdDeviation="6"/></filter>
    <filter id="frost" x="-15%" y="-40%" width="130%" height="180%" color-interpolation-filters="sRGB">
      <feGaussianBlur stdDeviation="1.4"/>
    </filter>
    <filter id="grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="17" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0"/>
      <feComponentTransfer><feFuncA type="table" tableValues="0 .11"/></feComponentTransfer>
    </filter>
  </defs>"""


# --------------------------------------------------------------------------
# Motion
#
# Every animation is CSS. SMIL would keep running - and keep the browser
# repainting - even for readers who asked for reduced motion, because no media
# query can switch it off.
#
# An SVG loaded through <img> is re-rasterised whole on every animation frame,
# filters included, so a smooth 60fps loop costs about a core per card. Stepped
# timing fixes the update rate instead: the two system pieces run a slow loop at
# a few updates a second, and the cards animate once, when they are first
# painted, then rest at zero cost.
# --------------------------------------------------------------------------

# One loop length and one step grid per asset. Sharing the grid matters: a
# repaint costs the same whether one element moved or five, so every animation
# in a file has to land on the same frames. Five animations stepping on five
# different phases would cost five times as much as one.
LOOP_DUR = 12.0    # the looping hero and flow
LOOP_GRID = 60     # 5 updates a second
CARD_DUR = 5.4     # one activation, played when a card is first painted
CARD_GRID = 40     # ~7.4 updates a second


def keyframes(name: str, grid: int, stops: list[tuple[float, str]]) -> str:
    """A keyframe rule pinned to the asset's step grid.

    `stops` are (fraction of the loop, declarations). Fractions snap to the
    grid, and an interval where nothing changes collapses to a single step, so
    a held pose costs no repaints at all.
    """
    snapped = [(max(0, min(grid, round(fraction * grid))), declaration)
               for fraction, declaration in stops]
    rules = []
    for index, (step, declaration) in enumerate(snapped):
        percent = step / grid * 100
        if index + 1 < len(snapped):
            span = max(1, snapped[index + 1][0] - step)
            count = 1 if snapped[index + 1][1] == declaration else span
            rules.append(f"{percent:.4g}% {{ {declaration}; animation-timing-function: steps({count}); }}")
        else:
            rules.append(f"{percent:.4g}% {{ {declaration}; }}")
    return f"    @keyframes {name} {{ {' '.join(rules)} }}\n"


def on_grid(seconds: float, duration: float, grid: int) -> float:
    """Snap a delay to the step grid so a delayed animation shares the frames."""
    step = duration / grid
    return round(seconds / step) * step


def rule(selector: str, declarations: str) -> str:
    return f"    {selector} {{ {declarations}; }}\n"


def travelling(css_class: str, path: str, name: str, duration: float,
               repeat: str = "infinite", delay: float = 0) -> str:
    """Bind a particle to a path. `offset-distance` is what the keyframes move."""
    hold = f" animation-delay: {delay:g}s;" if delay else ""
    return (f'    .{css_class} {{ offset-path: path("{path}"); offset-rotate: 0deg; '
            f'offset-distance: 0%; opacity: 0; animation: {name} {duration:g}s {repeat};{hold} }}\n')


def style(extra: str = "") -> str:
    return f"""  <style>
    .s {{ font-family: {SANS}; }}
    .m {{ font-family: {MONO}; }}
    .eyebrow {{ letter-spacing: .22em; }}
    .track {{ letter-spacing: .12em; }}
    .still {{ display: none; }}
    .mv {{ transform-box: fill-box; transform-origin: 50% 50%; }}
{extra}    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
      .motion {{ display: none !important; }}
      .still {{ display: inline !important; }}
    }}
  </style>"""


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------

def tube(d: str, width: float, gradient: str = "glass", gloss: str = "glossL",
         opacity: float = .86, sheen: bool = True, cls: str = "") -> str:
    """A chunky translucent tube along a path."""
    inner = ""
    if sheen:
        inner = (f'<path d="{d}" fill="none" stroke="#F2FFFC" stroke-width="{width * .26:.1f}" '
                 f'stroke-linecap="round" opacity=".14" transform="translate({-width * .09:.1f} {-width * .11:.1f})"/>')
    cls = f' class="{cls}"' if cls else ""
    return (f'<g{cls} filter="url(#{gloss})" opacity="{opacity:g}">'
            f'<path d="{d}" fill="none" stroke="url(#{gradient})" stroke-width="{width:g}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>{inner}</g>')


def solid(d: str, gradient: str = "glass", gloss: str = "glossL",
          opacity: float = .88, cls: str = "") -> str:
    """A chunky translucent filled form."""
    cls = f' class="{cls}"' if cls else ""
    return (f'<g{cls} filter="url(#{gloss})" opacity="{opacity:g}">'
            f'<path d="{d}" fill="url(#{gradient})"/></g>')


def sphere(cx: float, cy: float, r: float, gradient: str = "core",
           gloss: str = "glossM", opacity: float = 1.0, cls: str = "") -> str:
    cls = f' class="{cls}"' if cls else ""
    return (f'<g{cls} filter="url(#{gloss})" opacity="{opacity:g}">'
            f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="url(#{gradient})"/></g>')


def contact_shadow(cx: float, cy: float, rx: float, ry: float, opacity: float = .9) -> str:
    """Light pool plus the occlusion that sits in it, so the form feels grounded."""
    return (f'<ellipse cx="{cx:g}" cy="{cy:g}" rx="{rx * 1.55:g}" ry="{ry * 2.1:g}" fill="url(#pool)" opacity=".5"/>'
            f'<ellipse cx="{cx:g}" cy="{cy:g}" rx="{rx:g}" ry="{ry:g}" fill="#010403" opacity="{opacity:g}" filter="url(#shade)"/>')


def text(x: float, y: float, value: str, size: float, fill: str = WHITE, weight: int = 400,
         cls: str = "s", anchor: str = "start", opacity: float | None = None,
         extra: str = "") -> str:
    op = f' opacity="{opacity:g}"' if opacity is not None else ""
    anc = f' text-anchor="{anchor}"' if anchor != "start" else ""
    wt = f' font-weight="{weight}"' if weight != 400 else ""
    return (f'<text class="{cls}" x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{fill}"{wt}{anc}{op}{extra}>'
            f'{value}</text>')


def studio(width: int, height: int, label: str, index: str, radius: int = 30) -> str:
    """Black studio field, hairline frame and the editorial slug line."""
    border = "" if radius == 0 else (
        f'<rect x=".75" y=".75" width="{width - 1.5}" height="{height - 1.5}" rx="{radius - .75}" '
        f'fill="none" stroke="{BORDER}" stroke-width="1.5"/>')
    return f"""
  <rect width="{width}" height="{height}" rx="{radius}" fill="url(#vignette)"/>
  {border}
  {text(60, 50, label, 15, DIM, 500, cls="m eyebrow")}
  {text(width - 60, 50, index, 15, DIM, 500, cls="m eyebrow", anchor="end")}"""


def grain(width: int, height: int, radius: int = 30, opacity: float = .55) -> str:
    return (f'<rect width="{width}" height="{height}" rx="{radius}" filter="url(#grain)" '
            f'opacity="{opacity:g}" pointer-events="none"/>')


def write_svg(path: str, width: int, height: int, title: str, desc: str, body: str,
              css: str = "") -> None:
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">
  <title id="t">{title}</title>
  <desc id="d">{desc}</desc>
{defs()}
{style(css)}
{body}
</svg>
"""
    # Optional parts leave blank indented lines behind; keep the output tidy.
    tidy = "\n".join(line.rstrip() for line in document.splitlines() if line.strip())
    destination.write_text(tidy + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# Hero sculpture: the orbit and the abstract A
# --------------------------------------------------------------------------

# The hero sculpture lives in its own centred coordinate system so it can be
# placed and scaled into the hero, the mobile hero and the social preview.
RING_RX, RING_RY, RING_TILT = 248, 98, -15
RING_BACK = f"M{-RING_RX} 0A{RING_RX} {RING_RY} 0 0 1 {RING_RX} 0"
RING_FRONT = f"M{RING_RX} 0A{RING_RX} {RING_RY} 0 0 1 {-RING_RX} 0"
# One continuous caret: both legs of the A are a single inflated form.
A_LEGS = "M-116 196C-104 76-66-66-8-186C48-66 96 76 110 196"
A_BAR = "M-80 44C-30 26 42 26 92 42"


def _ring(half: str, width: float) -> str:
    """Half of the tilted glass ring, with a particle travelling inside it."""
    d = RING_BACK if half == "back" else RING_FRONT
    body = tube(d, width, "glassBack" if half == "back" else "glass", "glossM",
                .74 if half == "back" else .82)
    particle = (f'<g class="motion"><circle class="orbit-{half}" r="7" fill="{LIME}" filter="url(#bloomS)"/>'
                f'<circle class="orbit-{half}" r="3" fill="#FFFFFF"/></g>')
    return (f'<g transform="translate(0 30) rotate({RING_TILT})">{body}{particle}</g>')


HERO_CSS = (
    rule(".hero-form", f"animation: heroFloat {LOOP_DUR:g}s infinite")
    + rule(".hero-sat", f"animation: heroSat {LOOP_DUR:g}s infinite")
    + rule(".hero-haze", f"animation: heroHaze {LOOP_DUR:g}s infinite")
    + travelling("orbit-back", RING_BACK, "orbitBack", LOOP_DUR)
    + travelling("orbit-front", RING_FRONT, "orbitFront", LOOP_DUR)
    + keyframes("heroFloat", LOOP_GRID, [
        (0, "transform: translate(0, 0) rotate(0deg)"),
        (.5, "transform: translate(0, -9px) rotate(.5deg)"),
        (1, "transform: translate(0, 0) rotate(0deg)")])
    + keyframes("heroSat", LOOP_GRID, [
        (0, "transform: translate(0, 0)"),
        (.5, "transform: translate(-4px, 7px)"),
        (1, "transform: translate(0, 0)")])
    + keyframes("heroHaze", LOOP_GRID, [
        (0, "opacity: .55"), (.5, "opacity: 1"), (1, "opacity: .55")])
    + keyframes("orbitBack", LOOP_GRID, [
        (0, "offset-distance: 0%; opacity: 0"),
        (.04, "offset-distance: 4%; opacity: 1"),
        (.48, "offset-distance: 100%; opacity: 1"),
        (.5, "offset-distance: 100%; opacity: 0"),
        (1, "offset-distance: 100%; opacity: 0")])
    + keyframes("orbitFront", LOOP_GRID, [
        (0, "offset-distance: 0%; opacity: 0"),
        (.5, "offset-distance: 0%; opacity: 0"),
        (.54, "offset-distance: 4%; opacity: 1"),
        (.96, "offset-distance: 100%; opacity: 1"),
        (1, "offset-distance: 100%; opacity: 0")])
)


def hero_sculpture(cx: float, cy: float, scale: float = 1.0) -> tuple[str, str]:
    """Returns (behind, front) layers of the orbit sculpture, centred on (cx, cy)."""
    open_g = f'<g transform="translate({cx:g} {cy:g}) scale({scale:g})">'
    behind = f"""{open_g}
    <ellipse cy="10" rx="300" ry="250" fill="url(#haze)" class="hero-haze" opacity=".55"/>
    {contact_shadow(-98, 214, 62, 9, .9)}
    {contact_shadow(96, 214, 62, 9, .9)}
    {_ring("back", 30)}
  </g>"""
    front = f"""{open_g}
    <g class="mv hero-form">
      {tube(A_LEGS, 62, "glass", "glossL", .9)}
      {sphere(4, -18, 36, "core", "glossM")}
      {tube(A_BAR, 38, "glassLime", "glossM", .72)}
    </g>
    {_ring("front", 34)}
    <g class="mv hero-sat">
      {sphere(202, -70, 19, "coreLime", "glossS", .95)}
      {sphere(-214, 104, 13, "core", "glossS", .9)}
    </g>
    <g class="still"><circle cx="-150" cy="86" r="7" fill="{LIME}" filter="url(#bloomS)"/></g>
  </g>"""
    return behind, front


def build_hero() -> None:
    width, height = 1200, 560
    behind, front = hero_sculpture(878, 296, .90)
    body = f"""{studio(width, height, "Abdulelah Alkhathami", "Neural orbit / 01")}
  {behind}
  {text(72, 122, "AI systems engineering", 16, AQUA, 600, cls="m eyebrow")}
  {text(72, 208, "I engineer AI systems", 58, WHITE, 700, extra=' letter-spacing="-1.6"')}
  {text(72, 276, "that think, act, and", 48, WHITE, 600, extra=' letter-spacing="-1.2" opacity=".93"')}
  {text(72, 340, "earn trust.", 48, "url(#inkFade)", 700, extra=' letter-spacing="-1.2"')}
  <path d="M74 384H724" stroke="url(#hair)" stroke-width="1.5"/>
  {text(72, 428, "AI Agents · Voice AI · RAG · Product Engineering", 21, "#C3D8D2")}
  {text(72, 468, "Arabic-first systems · authorization outside the model", 18, MUTED)}
  {front}
  {grain(width, height)}"""
    write_svg("assets/profile/hero.svg", width, height,
              "Abdulelah Alkhathami — I engineer AI systems that think, act, and earn trust.",
              "A sculptural translucent letter A holding a luminous core, encircled by a tilted glass orbit "
              "ring on a black studio field. Illuminated particles travel inside the ring. Beside it: AI "
              "Agents, Voice AI, RAG and product engineering, Arabic-first, with authorization kept outside "
              "the model.",
              body, css=HERO_CSS)


def build_hero_mobile() -> None:
    width, height = 760, 860
    behind, front = hero_sculpture(380, 286, .72)
    body = f"""{studio(width, height, "Abdulelah Alkhathami", "01", radius=26)}
  {behind}
  {front}
  {text(56, 566, "AI systems engineering", 24, AQUA, 600, cls="m eyebrow")}
  {text(56, 646, "I engineer AI", 62, WHITE, 700, extra=' letter-spacing="-1.6"')}
  {text(56, 706, "systems that think,", 46, WHITE, 600, extra=' letter-spacing="-1"')}
  {text(56, 764, "act, and earn trust.", 46, "url(#inkFade)", 700, extra=' letter-spacing="-1"')}
  <path d="M58 800H520" stroke="url(#hair)" stroke-width="1.5"/>
  {text(56, 834, "AI Agents · Voice AI · RAG · Product Engineering", 22, "#C3D8D2")}
  {grain(width, height, radius=26)}"""
    write_svg("assets/profile/hero-mobile.svg", width, height,
              "Abdulelah Alkhathami — I engineer AI systems that think, act, and earn trust.",
              "Portrait version of the hero: a sculptural translucent letter A holding a luminous core "
              "inside a tilted glass orbit ring, above the statement and the practice areas.",
              body, css=HERO_CSS)


# --------------------------------------------------------------------------
# Accountable agent flow
# --------------------------------------------------------------------------

FLOW_STAGES = [
    ("01", "Intent", 148),
    ("02", "Reason", 372),
    ("03", "Authorize", 600),
    ("04", "Act", 838),
    ("05", "Verify", 1058),
]



def flow_conduit(y: float) -> str:
    return (f"M148 {y}C240 {y - 34} 288 {y + 30} 372 {y}S512 {y - 34} 600 {y}"
            f"S724 {y + 32} 838 {y}S972 {y - 32} 1058 {y}")


def authorization_gate(cx: float, cy: float, scale: float = 1.0, vertical: bool = False) -> str:
    """The boundary: a cold machined monolith split by a seam the conduit runs through.

    Materially different from the warm translucent stages - denser, colder, and
    the only element in the system with a hard structural seam.
    """
    rotation = " rotate(90)" if vertical else ""
    seam = f"""<g class="seam" opacity=".45">
      <path d="M-8-58V58" stroke="{LIME}" stroke-width="13" stroke-linecap="round" filter="url(#bloomS)"/>
      <path d="M-8-58V58" stroke="#F4FFF9" stroke-width="4" stroke-linecap="round"/>
    </g>"""
    return f"""<g transform="translate({cx:g} {cy:g}) scale({scale:g}){rotation}">
    <ellipse rx="128" ry="104" fill="url(#hazeLime)" opacity=".45"/>
    <g filter="url(#glossL)" opacity=".96">
      <rect x="-70" y="-72" width="56" height="144" rx="22" fill="url(#glassCold)"/>
      <rect x="14" y="-72" width="56" height="144" rx="22" fill="url(#glassCold)"/>
    </g>
    <g filter="url(#glossS)" opacity=".7">
      <rect x="-76" y="-88" width="152" height="17" rx="8.5" fill="url(#glassCold)"/>
      <rect x="-76" y="71" width="152" height="17" rx="8.5" fill="url(#glassCold)"/>
    </g>
    {seam}
  </g>"""


def pulse_ring(x: float, y: float, r: float, index: int, color: str = CYAN) -> str:
    """A stage ring that ignites as the signal reaches it."""
    return (f'<g class="motion"><circle class="mv pulse pulse-{index}" cx="{x:g}" cy="{y:g}" r="{r:g}" '
            f'fill="none" stroke="{color}" stroke-width="2.5" filter="url(#bloomS)" opacity="0"/></g>')


def signal(radius: float) -> str:
    """The illuminated request: it travels, halts at the boundary, then continues."""
    return (f'<g class="motion">'
            f'<circle class="signal" r="{radius:g}" fill="{LIME}" filter="url(#bloomS)"/>'
            f'<circle class="signal" r="{radius * .45:g}" fill="#FFFFFF"/></g>')


def flow_css(conduit: str) -> str:
    """Motion for one flow diagram: one signal, one seam, four stage rings."""
    css = travelling("signal", conduit, "flowSignal", LOOP_DUR)
    css += rule(".seam", f"animation: seam {LOOP_DUR:g}s infinite")
    css += rule(".pulse", f"animation: stagePulse {LOOP_DUR:g}s infinite")
    for index, arrival in enumerate(FLOW_ARRIVALS):
        if index != 2:
            delay = on_grid(arrival * LOOP_DUR, LOOP_DUR, LOOP_GRID)
            css += rule(f".pulse-{index}", f"animation-delay: {delay:.3f}s")
    css += keyframes("flowSignal", LOOP_GRID, [
        (0, "offset-distance: 0%; opacity: 0"),
        (.03, "offset-distance: 2%; opacity: 1"),
        (.30, "offset-distance: 49%; opacity: 1"),
        (.44, "offset-distance: 49%; opacity: 1"),
        (.46, "offset-distance: 49%; opacity: .3"),
        (.52, "offset-distance: 53%; opacity: 1"),
        (.86, "offset-distance: 100%; opacity: 1"),
        (.92, "offset-distance: 100%; opacity: 1"),
        (1, "offset-distance: 100%; opacity: 0")])
    css += keyframes("seam", LOOP_GRID, [
        (0, "opacity: .45"), (.28, "opacity: .45"), (.36, "opacity: 1"),
        (.54, "opacity: 1"), (.62, "opacity: .5"), (1, "opacity: .45")])
    css += keyframes("stagePulse", LOOP_GRID, [
        (0, "opacity: 0; transform: scale(1)"),
        (.03, "opacity: .75; transform: scale(1.4)"),
        (.09, "opacity: 0; transform: scale(1.75)"),
        (1, "opacity: 0; transform: scale(1.75)")])
    return css


# Fractions of the loop at which the signal reaches each stage. It waits at the
# authorization boundary from 0.30 to 0.52.
FLOW_ARRIVALS = (.02, .15, .33, .69, .86)


def build_flow() -> None:
    width, height = 1200, 440
    y = 258
    conduit = flow_conduit(y)
    gate_x = FLOW_STAGES[2][2]
    parts = []
    for index, (number, name, x) in enumerate(FLOW_STAGES):
        if name != "Authorize":
            radius = 26 if name in ("Intent", "Verify") else 22
            parts.append(sphere(x, y, radius, "core", "glossM", .95))
            parts.append(pulse_ring(x, y, radius + 12, index))
        parts.append(text(x, y + 104, number, 14, DIM, 500, cls="m eyebrow", anchor="middle"))
        parts.append(text(x, y + 130, name, 18, LIME if name == "Authorize" else WHITE, 600,
                          cls="s track", anchor="middle"))
    body = f"""{studio(width, height, "Accountable agent flow", "System / 02")}
  {text(60, 112, "The model proposes. The application decides.", 30, WHITE, 600)}
  {text(60, 148, "Every sensitive action stops at a boundary the model does not own.", 19, MUTED)}
  <ellipse cx="600" cy="{y}" rx="540" ry="118" fill="url(#haze)" opacity=".5" class="seam"/>
  {contact_shadow(600, y + 92, 360, 10, .7)}
  <path d="{conduit}" fill="none" stroke="#061F1A" stroke-width="44" stroke-linecap="round"/>
  {tube(conduit, 30, "glass", "glossM", .78, sheen=False)}
  <path d="{conduit}" fill="none" stroke="#EBFFFB" stroke-width="2.5" stroke-linecap="round" opacity=".28"
        transform="translate(-2 -6)"/>
  {signal(11)}
  <g class="still"><circle cx="{gate_x - 104}" cy="{y - 14}" r="11" fill="{LIME}" filter="url(#bloomS)"/>
    <circle cx="{gate_x - 104}" cy="{y - 14}" r="5" fill="#FFFFFF"/></g>
  {''.join(parts)}
  {authorization_gate(gate_x, y, .82)}
  {text(gate_x, y + 156, "owned by the application", 13, DIM, 400, cls="m", anchor="middle")}
  {grain(width, height)}"""
    write_svg("assets/profile/system-flow.svg", width, height,
              "Accountable agent flow: intent, reason, authorize, act, verify",
              "One translucent conduit carries an illuminated signal through five stages. At Authorize the "
              "signal halts inside a cold machined monolith - the boundary owned by the application, not "
              "the model - then continues to Act and Verify.",
              body, css=flow_css(conduit))


def build_flow_mobile() -> None:
    width, height = 760, 980
    top = 236
    gap = 148
    x = 262
    conduit = (f"M{x} {top}C{x - 40} {top + 62} {x + 40} {top + 86} {x} {top + gap}"
               f"S{x - 40} {top + gap + 86} {x} {top + 2 * gap}"
               f"S{x + 40} {top + 2 * gap + 86} {x} {top + 3 * gap}"
               f"S{x - 40} {top + 3 * gap + 86} {x} {top + 4 * gap}")
    parts = []
    for index, (number, name, _) in enumerate(FLOW_STAGES):
        y = top + index * gap
        if name != "Authorize":
            parts.append(sphere(x, y, 30, "core", "glossM", .95))
            parts.append(pulse_ring(x, y, 44, index))
        parts.append(text(400, y - 8, number, 20, DIM, 500, cls="m eyebrow"))
        parts.append(text(400, y + 28, name, 34, LIME if name == "Authorize" else WHITE, 600, cls="s track"))
    body = f"""{studio(width, height, "Accountable agent flow", "02", radius=26)}
  {text(56, 122, "The model proposes.", 38, WHITE, 700)}
  {text(56, 172, "The application decides.", 38, "url(#inkFade)", 700)}
  <ellipse cx="{x}" cy="{top + 2 * gap}" rx="300" ry="400" fill="url(#haze)" opacity=".45"/>
  <path d="{conduit}" fill="none" stroke="#061F1A" stroke-width="46" stroke-linecap="round"/>
  {tube(conduit, 30, "glass", "glossM", .68, sheen=False)}
  {signal(13)}
  <g class="still"><circle cx="{x - 30}" cy="{top + 2 * gap - 104}" r="13" fill="{LIME}" filter="url(#bloomS)"/></g>
  {''.join(parts)}
  {authorization_gate(x, top + 2 * gap, .78, vertical=True)}
  {grain(width, height, radius=26)}"""
    write_svg("assets/profile/system-flow-mobile.svg", width, height,
              "Accountable agent flow: intent, reason, authorize, act, verify",
              "Portrait version: one translucent conduit carries an illuminated signal down through intent, "
              "reason, authorize, act and verify. The signal halts at the cold authorization monolith.",
              body, css=flow_css(conduit))


# --------------------------------------------------------------------------
# Product layers
# --------------------------------------------------------------------------

LAYERS = [
    ("Experience", "Arabic / English UX · workflow design · clear failure states", "glassCold"),
    ("Application", "Python · FastAPI · TypeScript · Next.js · Pydantic · Zod", "glass"),
    ("Intelligence", "Tool calling · RAG · embeddings · structured outputs", "glassLime"),
    ("Infrastructure", "PostgreSQL · pgvector · Redis · Docker · local inference", "glassBack"),
]


def slab(cx: float, cy: float, half_w: float, half_d: float, thickness: float,
         gradient: str, opacity: float = .82) -> str:
    """An axonometric chunky slab; the gloss filter bevels and inflates it."""
    outline = (f"M{cx:g} {cy - half_d:g}L{cx + half_w:g} {cy:g}L{cx + half_w:g} {cy + thickness:g}"
               f"L{cx:g} {cy + half_d + thickness:g}L{cx - half_w:g} {cy + thickness:g}"
               f"L{cx - half_w:g} {cy:g}Z")
    top = (f"M{cx:g} {cy - half_d:g}L{cx + half_w:g} {cy:g}L{cx:g} {cy + half_d:g}"
           f"L{cx - half_w:g} {cy:g}Z")
    right = (f"M{cx + half_w:g} {cy:g}L{cx + half_w:g} {cy + thickness:g}"
             f"L{cx:g} {cy + half_d + thickness:g}L{cx:g} {cy + half_d:g}Z")
    return (f'<g filter="url(#glossL)" opacity="{opacity:g}">'
            f'<path d="{outline}" fill="url(#{gradient})"/>'
            f'<path d="{top}" fill="#EAFFFB" opacity=".22"/>'
            f'<path d="{right}" fill="#02110E" opacity=".35"/></g>')




def layer_cascade() -> str:
    """Light travelling down the spine, pausing inside each layer."""
    return f'<g class="motion"><circle class="cascade" r="9" fill="{LIME}" filter="url(#bloomS)"/></g>'


def layers_css(spine: str) -> str:
    """One activation: the slabs settle in order, then light runs down the spine."""
    css = travelling("cascade", spine, "cascade", CARD_DUR, repeat="1 both")
    css += rule(".slab", f"animation: slabIn {CARD_DUR:g}s 1 both")
    css += "".join(
        rule(f".slab-{i}", f"animation-delay: {on_grid(i * .22, CARD_DUR, CARD_GRID):.3f}s")
        for i in range(4))
    css += keyframes("cascade", CARD_GRID, [
        (0, "offset-distance: 0%; opacity: 0"),
        (.3, "offset-distance: 4%; opacity: 0"),
        (.36, "offset-distance: 12%; opacity: 1"),
        (.62, "offset-distance: 52%; opacity: 1"),
        (.9, "offset-distance: 100%; opacity: 1"),
        (1, "offset-distance: 100%; opacity: 0")])
    css += keyframes("slabIn", CARD_GRID, [
        (0, "opacity: .62; transform: translateY(-9px)"),
        (.34, "opacity: 1; transform: translateY(0)"),
        (1, "opacity: 1; transform: translateY(0)")])
    return css


def build_layers() -> None:
    width, height = 1200, 470
    top_y = 200
    step = 58
    cx = 300
    half_w, half_d, thickness = 130, 54, 20

    spine = f"M{cx} {top_y - 48}V{top_y + 3 * step + 66}"
    stack, labels, links = [], [], []
    for index, (name, detail, gradient) in enumerate(LAYERS):
        y = top_y + index * step
        stack.append(f'<g class="mv slab slab-{index}">'
                     f'{slab(cx, y, half_w, half_d, thickness, gradient, .82 - index * .05)}</g>')
        label_y = 152 + index * 76
        labels.append(text(640, label_y, name, 25, WHITE, 600))
        labels.append(text(640, label_y + 26, detail, 16, MUTED))
        links.append(f'<path d="M{cx + half_w - 6} {y + 16}C{cx + half_w + 90} {y + 16} {540} {label_y - 8} {616} {label_y - 8}" '
                     f'fill="none" stroke="{AQUA}" stroke-opacity=".22" stroke-width="1.5"/>')
        links.append(f'<circle cx="616" cy="{label_y - 8}" r="3.5" fill="{AQUA}" opacity=".65"/>')

    body = f"""{studio(width, height, "Product layers", "System / 03")}
  {text(60, 112, "One product. Four engineered layers.", 30, WHITE, 600)}
  <ellipse cx="{cx}" cy="{top_y + 84}" rx="290" ry="220" fill="url(#haze)" opacity=".5"/>
  {contact_shadow(cx, top_y + 3 * step + 92, 150, 12, .8)}
  <path d="{spine}" stroke="#0C3A33" stroke-width="15" stroke-linecap="round"/>
  <path d="{spine}" stroke="url(#glass)" stroke-width="6" stroke-linecap="round" opacity=".45"/>
  {''.join(stack)}
  {layer_cascade()}
  {''.join(links)}
  {''.join(labels)}
  {grain(width, height)}"""
    write_svg("assets/profile/system-layers.svg", width, height,
              "Four engineered layers: experience, application, intelligence, infrastructure",
              "Four chunky translucent slabs stacked in depth - experience, application, intelligence and "
              "infrastructure - threaded by a glass spine that carries light down through every layer.",
              body, css=layers_css(spine))


def build_layers_mobile() -> None:
    width, height = 760, 900
    top_y = 300
    step = 140
    cx = 330
    spine = f"M{cx} {top_y - 110}V{top_y + 3 * step + 150}"
    parts = []
    for index, (name, detail, gradient) in enumerate(LAYERS):
        y = top_y + index * step
        parts.append(f'<g class="mv slab slab-{index}">'
                     f'{slab(cx, y, 150, 78, 30, gradient, .82 - index * .05)}</g>')
        parts.append(text(524, y + 10, name, 26, WHITE, 600))
    body = f"""{studio(width, height, "Product layers", "03", radius=26)}
  {text(56, 126, "One product.", 40, WHITE, 700)}
  {text(56, 178, "Four engineered layers.", 40, "url(#inkFade)", 700)}
  <ellipse cx="{cx}" cy="{top_y + 190}" rx="330" ry="340" fill="url(#haze)" opacity=".45"/>
  {contact_shadow(cx, top_y + 3 * step + 138, 168, 13, .8)}
  <path d="{spine}" stroke="#0C3A33" stroke-width="18" stroke-linecap="round"/>
  <path d="{spine}" stroke="url(#glass)" stroke-width="7" stroke-linecap="round" opacity=".45"/>
  {''.join(parts)}
  {layer_cascade()}
  {grain(width, height, radius=26)}"""
    write_svg("assets/profile/system-layers-mobile.svg", width, height,
              "Four engineered layers: experience, application, intelligence, infrastructure",
              "Portrait version: four chunky translucent slabs stacked in depth and threaded by a glass "
              "spine that carries light down through every layer.",
              body, css=layers_css(spine))


# --------------------------------------------------------------------------
# Project sculptures
# --------------------------------------------------------------------------

def sculpture_threshold(cx: float, cy: float, scale: float = 1.0) -> str:
    """Raqmi: a protected transition. The payload crosses once the threshold ignites."""
    arch = "M-104 148V22A104 96 0 0 1 104 22V148"
    threshold = (f'<path d="M-74 136H74" stroke="{LIME}" stroke-width="15" stroke-linecap="round" filter="url(#bloomS)"/>'
                 f'<path d="M-74 136H74" stroke="{LIME}" stroke-width="7" stroke-linecap="round"/>'
                 f'<path d="M-74 136H74" stroke="#F4FFF9" stroke-width="2.5" stroke-linecap="round"/>')
    return f"""<g transform="translate({cx:g} {cy:g}) scale({scale:g})">
    <ellipse cy="10" rx="250" ry="190" fill="url(#haze)" opacity=".7"/>
    {contact_shadow(0, 162, 132, 11, .85)}
    <g transform="translate(150 74)"><g class="mv payload">{sphere(0, 0, 36, "coreLime", "glossM")}</g></g>
    {tube(arch, 44, "glassCold", "glossL", .92)}
    <g class="threshold">{threshold}</g>
  </g>"""


THRESHOLD_CSS = (
    rule(".payload", f"animation: payloadCross {CARD_DUR:g}s 1 both")
    + rule(".threshold", f"animation: thresholdWake {CARD_DUR:g}s 1 both")
    + keyframes("payloadCross", CARD_GRID, [
        (0, "transform: translateX(-300px); opacity: 0"),
        (.1, "transform: translateX(-300px); opacity: 1"),
        (.34, "transform: translateX(-300px); opacity: 1"),
        (.64, "transform: translateX(-112px); opacity: 1"),
        (1, "transform: translateX(0px); opacity: 1")])
    + keyframes("thresholdWake", CARD_GRID, [
        (0, "opacity: .45"), (.32, "opacity: .45"), (.46, "opacity: 1"), (1, "opacity: 1")])
)


def sculpture_dialogue(cx: float, cy: float, scale: float = 1.0) -> str:
    """Abdulelah.de: two forms turning around one shared source of truth."""
    arm = "M-178 34C-206-64-134-140-56-114C4-94 26-34 4 16"
    trail = "M-150-84C-78-62-40-22-6-2"
    return f"""<g transform="translate({cx:g} {cy:g}) scale({scale:g})">
    <ellipse rx="250" ry="180" fill="url(#haze)" opacity=".7"/>
    {contact_shadow(0, 158, 140, 11, .85)}
    {tube(arm, 52, "glassBack", "glossM", .78)}
    <g transform="rotate(180)">{tube(arm, 56, "glass", "glossL", .9)}</g>
    <g class="motion"><circle class="spark-a" r="7" fill="{LIME}" filter="url(#bloomS)"/></g>
    <g transform="rotate(180)" class="motion"><circle class="spark-b" r="7" fill="{CYAN}" filter="url(#bloomS)"/></g>
    <g class="core-wake">
      {sphere(0, 0, 48, "core", "glossM")}
      <circle cx="-15" cy="-17" r="10" fill="#FFFFFF" opacity=".5" filter="url(#bloomS)"/>
    </g>
    <circle cx="-88" cy="-52" r="7" fill="{LIME}" filter="url(#bloomS)" opacity=".85"/>
    <circle cx="88" cy="52" r="7" fill="{CYAN}" filter="url(#bloomS)" opacity=".85"/>
  </g>"""


DIALOGUE_CSS = (
    travelling("spark-a", "M-150-84C-78-62-40-22-6-2", "sparkIn", CARD_DUR, repeat="1 both")
    + travelling("spark-b", "M-150-84C-78-62-40-22-6-2", "sparkIn", CARD_DUR, repeat="1 both",
                 delay=on_grid(CARD_DUR * .28, CARD_DUR, CARD_GRID))
    + rule(".core-wake", f"animation: coreWake {CARD_DUR:g}s 1 both")
    + keyframes("sparkIn", CARD_GRID, [
        (0, "offset-distance: 0%; opacity: 0"),
        (.08, "offset-distance: 6%; opacity: 1"),
        (.52, "offset-distance: 100%; opacity: 1"),
        (.60, "offset-distance: 100%; opacity: 0"),
        (1, "offset-distance: 100%; opacity: 0")])
    + keyframes("coreWake", CARD_GRID, [
        (0, "opacity: .55"), (.5, "opacity: .55"), (.62, "opacity: 1"), (1, "opacity: 1")])
)


def sculpture_lattice(cx: float, cy: float, scale: float = 1.0) -> str:
    """ChatUB: a knowledge lattice that stays inside its own shell."""
    nodes = [(-84, -18, 19), (-20, -74, 15), (44, -26, 21), (-40, 52, 16), (58, 56, 13), (104, 6, 11)]
    links = [
        ("M-84-18C-58-44-44-60-20-74", 13),
        ("M-20-74C6-60 26-44 44-26", 12),
        ("M-84-18C-66 12-58 34-40 52", 12),
        ("M-40 52C-4 60 26 60 58 56", 11),
        ("M44-26C52 6 56 32 58 56", 11),
        ("M44-26C70-16 90-6 104 6", 9),
    ]
    lattice = "".join(tube(d, w, "glass", "glossS", .74, sheen=False) for d, w in links)
    spheres = "".join(
        f'<g class="mv node node-{i}">{sphere(x, y, r, "core", "glossS", .95)}</g>'
        for i, (x, y, r) in enumerate(nodes)
    )
    return f"""<g transform="translate({cx:g} {cy:g}) scale({scale:g})">
    <ellipse rx="250" ry="180" fill="url(#haze)" opacity=".7"/>
    {contact_shadow(0, 148, 140, 11, .85)}
    <g>
      <g transform="scale(1.14)"><g class="mesh">{lattice}</g>{spheres}</g>
      <ellipse cy="34" rx="156" ry="100" fill="url(#haze)" opacity=".95"/>
      <path d="M-178 104A178 150 0 0 1 178 104Z" fill="url(#glassCold)" opacity=".16"/>
      {tube("M-178 104A178 150 0 0 1 178 104", 36, "glass", "glossM", .6)}
      {slab(0, 116, 172, 20, 10, "glassBack", .62)}
    </g>
  </g>"""


LATTICE_CSS = (
    rule(".mesh", f"animation: meshWake {CARD_DUR:g}s 1 both")
    + rule(".node", f"animation: nodeWake {CARD_DUR:g}s 1 both")
    + "".join(
        rule(f".node-{i}", f"animation-delay: {on_grid(.2 + i * .34, CARD_DUR, CARD_GRID):.3f}s")
        for i in range(6))
    + keyframes("meshWake", CARD_GRID, [
        (0, "opacity: .5"), (.6, "opacity: 1"), (1, "opacity: 1")])
    + keyframes("nodeWake", CARD_GRID, [
        (0, "opacity: .45; transform: scale(.88)"),
        (.1, "opacity: 1; transform: scale(1.12)"),
        (.18, "opacity: 1; transform: scale(1)"),
        (1, "opacity: 1; transform: scale(1)")])
)


# slug, eyebrow, title, line, detail, short detail for the portrait card, sculpture, description
PROJECTS = [
    ("raqmi", "Agentic AI · bilingual support", "Raqmi", "Tool use with a boundary.",
     "Native tool calling · authorization outside the model · captured evaluation",
     "Tool calling · authorization · evaluation",
     sculpture_threshold, THRESHOLD_CSS,
     "Raqmi — a bounded passage sculpture: a luminous payload waits outside an arched glass threshold "
     "until the application authorizes it to cross."),
    ("portfolio", "AI product · bilingual web", "Abdulelah.de", "A portfolio you can ask.",
     "Next.js · typed project facts · server-side AI assistant",
     "Next.js · typed facts · AI assistant",
     sculpture_dialogue, DIALOGUE_CSS,
     "Abdulelah.de — two interlocking translucent forms turning around one shared luminous core, "
     "exchanging light in both directions."),
    ("chatub", "Local AI · Arabic retrieval", "ChatUB", "Knowledge, kept close.",
     "Arabic FAQ retrieval · semantic similarity · local generation with Ollama",
     "Arabic retrieval · local generation",
     sculpture_lattice, LATTICE_CSS,
     "ChatUB — a lattice of glass nodes lighting up in sequence beneath a frosted shell that keeps the "
     "knowledge local."),
]


def build_projects() -> None:
    width, height = 1200, 360
    for index, (slug, eyebrow, title, line, detail, short, sculpture, card_css, desc) in enumerate(PROJECTS, start=1):
        body = f"""{studio(width, height, eyebrow, f"Selected work / 0{index}")}
  {sculpture(908, 192, .80)}
  {text(60, 146, title, 54, WHITE, 700, extra=' letter-spacing="-1.4"')}
  {text(60, 200, line, 27, "url(#inkFade)", 600)}
  {text(60, 254, detail, 17, MUTED)}
  <path d="M62 292H430" stroke="url(#hair)" stroke-width="1.5"/>
  {text(60, 322, "Open the repository", 15, AQUA, 600, cls="m track")}
  {grain(width, height)}"""
        write_svg(f"assets/projects/{slug}.svg", width, height, f"{title} — {line}", desc, body,
                  css=card_css)

        mobile_width, mobile_height = 760, 640
        mobile = f"""{studio(mobile_width, mobile_height, eyebrow, f"0{index}", radius=26)}
  {sculpture(380, 246, .80)}
  {text(56, 456, title, 58, WHITE, 700, extra=' letter-spacing="-1.4"')}
  {text(56, 512, line, 32, "url(#inkFade)", 600)}
  {text(56, 566, short, 22, MUTED)}
  {grain(mobile_width, mobile_height, radius=26)}"""
        write_svg(f"assets/projects/{slug}-mobile.svg", mobile_width, mobile_height,
                  f"{title} — {line}", desc, mobile, css=card_css)


# --------------------------------------------------------------------------
# Social preview
# --------------------------------------------------------------------------

def build_social_preview() -> None:
    """The 1280x640 card GitHub shows when the profile is shared."""
    width, height = 1280, 640
    behind, front = hero_sculpture(956, 318, .92)
    # Short measures: on a wide fallback font the lines still stop short of the
    # sculpture, and the whole sculpture sits behind the type either way.
    headline = [
        (64, 258, "I engineer AI", 74, WHITE, 700, "-2.2"),
        (64, 340, "systems that think,", 58, WHITE, 600, "-1.6"),
        (64, 420, "act, and earn trust.", 58, "url(#inkFade)", 700, "-1.6"),
    ]

    def headline_text() -> str:
        return "".join(
            text(x, y, value, size, fill, weight, extra=f' letter-spacing="{tracking}"')
            for x, y, value, size, fill, weight, tracking in headline
        )

    body = f"""{studio(width, height, "Abdulelah Alkhathami", "AI systems", radius=0)}
  {behind}
  {front}
  {text(64, 152, "AI Agents · Voice AI · RAG · Product Engineering", 20, AQUA, 600, cls="m eyebrow")}
  {headline_text()}
  {text(64, 556, "Abdulelah Alkhathami", 26, WHITE, 600)}
  {text(64, 592, "abdulelah.de · Arabic-first AI systems", 20, MUTED, cls="m")}
  {grain(width, height, radius=0, opacity=.5)}"""
    write_svg("assets/profile/social-preview.svg", width, height,
              "Abdulelah Alkhathami — I engineer AI systems that think, act, and earn trust.",
              "Social preview: a sculptural translucent letter A holding a luminous core inside a glass "
              "orbit ring, beside the statement 'I engineer AI systems that think, act, and earn trust.'",
              body, css=HERO_CSS)


def main() -> None:
    builders = (
        build_hero, build_hero_mobile,
        build_flow, build_flow_mobile,
        build_layers, build_layers_mobile,
        build_projects,
        build_social_preview,
    )
    for builder in builders:
        builder()
    print("Generated the sculptural profile system.")


if __name__ == "__main__":
    main()
