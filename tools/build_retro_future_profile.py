#!/usr/bin/env python3
"""Generate the original retro-futuristic SVG system used by the profile README."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
P = {
    "black": "#030706", "white": "#f4fff9", "muted": "#91aaa3",
    "cyan": "#46f6ff", "aqua": "#22e3c5", "lime": "#c8ff54",
    "blue": "#3b65ff",
}


def defs(extra: str = "") -> str:
    return f"""
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{P['black']}"/><stop offset=".52" stop-color="#06100e"/><stop offset="1" stop-color="#020504"/></linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{P['cyan']}" stop-opacity=".95"/><stop offset=".28" stop-color="{P['aqua']}" stop-opacity=".62"/><stop offset=".64" stop-color="{P['lime']}" stop-opacity=".84"/><stop offset="1" stop-color="{P['blue']}" stop-opacity=".76"/></linearGradient>
    <linearGradient id="glassReverse" x1="1" y1="0" x2="0" y2="1"><stop stop-color="{P['lime']}" stop-opacity=".94"/><stop offset=".45" stop-color="{P['aqua']}" stop-opacity=".62"/><stop offset="1" stop-color="{P['blue']}" stop-opacity=".82"/></linearGradient>
    <radialGradient id="orb" cx="34%" cy="25%" r="74%"><stop stop-color="#efffff"/><stop offset=".16" stop-color="{P['cyan']}"/><stop offset=".52" stop-color="{P['aqua']}" stop-opacity=".75"/><stop offset=".78" stop-color="{P['blue']}" stop-opacity=".5"/><stop offset="1" stop-color="#031713" stop-opacity=".25"/></radialGradient>
    <radialGradient id="halo"><stop stop-color="{P['aqua']}" stop-opacity=".35"/><stop offset="1" stop-color="{P['aqua']}" stop-opacity="0"/></radialGradient>
    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="13" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="smallGlow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".88" numOctaves="3" seed="31" result="noise"/><feColorMatrix in="noise" type="saturate" values="0" result="mono"/><feComponentTransfer in="mono"><feFuncA type="table" tableValues="0 .12"/></feComponentTransfer></filter>
    <pattern id="microGrid" width="42" height="42" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#9fffea" opacity=".1"/></pattern>
{extra}
  </defs>"""


STYLE = """
  <style>
    text { font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; }
    .drift { transform-box: fill-box; transform-origin: center; animation: drift 7s ease-in-out infinite; }
    .drift-alt { transform-box: fill-box; transform-origin: center; animation: driftAlt 9s ease-in-out infinite; }
    .spin { transform-box: fill-box; transform-origin: center; animation: spin 18s linear infinite; }
    .pulse { animation: pulse 2.8s ease-in-out infinite; }
    .scan { stroke-dasharray: 6 18; animation: scan 3.2s linear infinite; }
    .blink { animation: blink 2.4s ease-in-out infinite; }
    @keyframes drift { 0%,100% { transform: translateY(0) rotate(-1deg); } 50% { transform: translateY(-10px) rotate(1.5deg); } }
    @keyframes driftAlt { 0%,100% { transform: translate(0,0) rotate(1deg); } 50% { transform: translate(8px,-7px) rotate(-1.3deg); } }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes pulse { 0%,100% { opacity:.42; } 50% { opacity:1; } }
    @keyframes scan { to { stroke-dashoffset:-96; } }
    @keyframes blink { 0%,100% { opacity:.32; } 50% { opacity:1; } }
    @media (prefers-reduced-motion: reduce) { .drift,.drift-alt,.spin,.pulse,.scan,.blink { animation:none !important; } }
  </style>"""


def frame(width: int, height: int, label: str) -> str:
    return f"""
  <rect width="{width}" height="{height}" rx="26" fill="url(#bg)"/>
  <rect width="{width}" height="{height}" rx="26" fill="url(#microGrid)"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="25" fill="none" stroke="#17352f"/>
  <text x="54" y="47" fill="{P['muted']}" font-size="13" font-weight="700" letter-spacing="3.2">{label}</text>
  <circle cx="{width - 56}" cy="43" r="4" fill="{P['lime']}" class="blink"/>
  <text x="{width - 72}" y="48" text-anchor="end" fill="{P['muted']}" font-size="11" letter-spacing="2">LIVE</text>"""


def grain(width: int, height: int) -> str:
    return f'<rect width="{width}" height="{height}" rx="26" filter="url(#grain)" opacity=".48" pointer-events="none"/>'


def write_svg(path: str, width: int, height: int, title: str, description: str, body: str) -> None:
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title><desc id="desc">{description}</desc>
{defs()}{STYLE}{body}
</svg>
""", encoding="utf-8")


def build_hero() -> None:
    width, height = 1200, 520
    path = "M777 364 C716 281 737 158 827 126 C916 94 1034 143 1055 233 C1072 309 1015 397 921 398 C855 399 805 366 799 310 C791 244 846 201 901 217 C947 231 966 283 939 321 C912 359 849 350 825 310"
    body = frame(width, height, "ABDULELAH / AI SYSTEMS") + f"""
  <text x="54" y="132" fill="{P['white']}" font-size="55" font-weight="750" letter-spacing="-1.5">I ENGINEER</text>
  <text x="54" y="202" fill="url(#glass)" font-size="73" font-weight="850" letter-spacing="-2.5">AI SYSTEMS</text>
  <text x="58" y="253" fill="{P['muted']}" font-size="19" letter-spacing="2.4">THAT THINK  ·  ACT  ·  EARN TRUST</text>
  <text x="58" y="319" fill="{P['white']}" font-size="19">AI Agents  /  Voice AI  /  RAG  /  Product Engineering</text>
  <path d="M58 353H524" stroke="#1a4c43"/>
  <text x="58" y="391" fill="{P['muted']}" font-size="15">Arabic-first products. Accountable by design.</text>
  <g transform="translate(58 429)"><rect width="164" height="38" rx="19" fill="#0b1b18" stroke="#24564c"/><circle cx="20" cy="19" r="5" fill="{P['lime']}" class="pulse"/><text x="35" y="24" fill="{P['white']}" font-size="13" font-weight="700" letter-spacing="1.2">BUILDING NOW</text></g>
  <ellipse cx="914" cy="264" rx="256" ry="232" fill="url(#halo)" opacity=".7"/>
  <g class="spin" opacity=".54"><ellipse cx="914" cy="264" rx="208" ry="155" fill="none" stroke="#2a6256" stroke-width="1.2" stroke-dasharray="3 13"/><circle cx="1122" cy="264" r="5" fill="{P['lime']}" filter="url(#smallGlow)"/></g>
  <g class="drift">
    <path d="{path}" fill="none" stroke="#011b17" stroke-width="94" stroke-linecap="round" stroke-linejoin="round" opacity=".78" filter="url(#softGlow)"/>
    <path d="{path}" fill="none" stroke="url(#glass)" stroke-width="72" stroke-linecap="round" stroke-linejoin="round" opacity=".86"/>
    <path d="{path}" fill="none" stroke="#e9ffff" stroke-width="9" stroke-linecap="round" opacity=".38" transform="translate(-7 -8)"/>
    <path d="{path}" fill="none" stroke="#2cfff0" stroke-width="3" stroke-linecap="round" opacity=".78" class="scan"/>
    <circle cx="921" cy="398" r="46" fill="url(#orb)" opacity=".92"/><circle cx="904" cy="380" r="10" fill="#fff" opacity=".58"/>
    <circle r="9" fill="{P['lime']}" filter="url(#smallGlow)"><animateMotion dur="5.2s" repeatCount="indefinite" path="{path}"/></circle>
  </g>
  <g class="drift-alt"><path d="M774 189 C825 124 912 95 1000 121" fill="none" stroke="url(#glassReverse)" stroke-width="28" stroke-linecap="round" opacity=".7"/><path d="M777 182 C825 125 906 101 991 125" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".32"/><circle cx="1000" cy="121" r="22" fill="url(#orb)"/></g>
  <text x="914" y="484" text-anchor="middle" fill="{P['muted']}" font-size="11" letter-spacing="3.4">NEURAL ORBIT / 01</text>
{grain(width, height)}"""
    write_svg("assets/profile/hero.svg", width, height, "Abdulelah Alkhathami — AI systems in motion", "A luminous retro-futuristic neural orbit accompanies the statement: I engineer AI systems that think, act, and earn trust.", body)


def build_flow() -> None:
    width, height = 1200, 360
    nodes = [(125, "01", "INTENT"), (355, "02", "REASON"), (600, "03", "AUTHORIZE"), (845, "04", "ACT"), (1075, "05", "VERIFY")]
    path = "M125 203 C225 143 266 263 355 203 S510 143 600 203 S755 263 845 203 S980 143 1075 203"
    body = frame(width, height, "ACCOUNTABLE AGENT FLOW") + f"""
  <text x="54" y="93" fill="{P['white']}" font-size="28" font-weight="760">From intent to verified outcome.</text>
  <text x="1146" y="92" text-anchor="end" fill="{P['muted']}" font-size="14">The model proposes. The application decides.</text>
  <path id="flowPath" d="{path}" fill="none" stroke="#103a32" stroke-width="38" stroke-linecap="round"/>
  <path d="{path}" fill="none" stroke="url(#glass)" stroke-opacity=".62" stroke-width="22" stroke-linecap="round"/>
  <path d="M125 197 C225 137 266 257 355 197 S510 137 600 197 S755 257 845 197 S980 137 1075 197" fill="none" stroke="#eaffff" stroke-opacity=".27" stroke-width="4" stroke-linecap="round"/>
  <circle r="10" fill="{P['lime']}" filter="url(#smallGlow)"><animateMotion dur="5.8s" repeatCount="indefinite"><mpath href="#flowPath"/></animateMotion></circle>
  <g transform="translate(600 203)"><circle r="67" fill="#031a15" stroke="#78ffdc" stroke-opacity=".34"/><circle r="48" fill="url(#orb)" opacity=".82" filter="url(#smallGlow)"/><path d="M-14-2v-12a14 14 0 0 1 28 0v12M-22-2h44v35h-44z" fill="none" stroke="#f1fff9" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>"""
    for x, number, label in nodes:
        if label != "AUTHORIZE":
            pulse = ' class="pulse"' if label in {"INTENT", "VERIFY"} else ""
            body += f'<g{pulse}><circle cx="{x}" cy="203" r="35" fill="#071a16" stroke="#75ffe1" stroke-opacity=".5"/><circle cx="{x}" cy="203" r="19" fill="url(#orb)" opacity=".9"/></g>'
        body += f'<text x="{x}" y="293" text-anchor="middle" fill="{P["muted"]}" font-size="11" letter-spacing="2.6">{number}</text><text x="{x}" y="321" text-anchor="middle" fill="{P["white"]}" font-size="14" font-weight="750" letter-spacing="1.8">{label}</text>'
    body += grain(width, height)
    write_svg("assets/profile/system-flow.svg", width, height, "Accountable AI agent flow", "A glowing signal travels from intent through reasoning, independent authorization, action, and verification.", body)


PROJECTS = [
    ("raqmi", "AGENTIC AI / BILINGUAL SUPPORT", "Raqmi", "Tool use with a boundary.", "Native tool calling · authorization outside the LLM · captured evaluation", "gate"),
    ("portfolio", "AI PRODUCT / BILINGUAL WEB", "Abdulelah.de", "A portfolio you can ask.", "Next.js · typed project facts · server-side AI assistant", "dialogue"),
    ("chatub", "LOCAL AI / ARABIC RETRIEVAL", "ChatUB", "Knowledge, kept close.", "Arabic FAQ retrieval · local generation · Ollama", "network"),
]


def sculpture(kind: str) -> str:
    if kind == "gate":
        return f"""<g class="drift"><ellipse cx="914" cy="156" rx="220" ry="125" fill="url(#halo)" opacity=".55"/><path d="M786 70 C728 96 729 218 790 244" fill="none" stroke="#06231d" stroke-width="74" stroke-linecap="round" filter="url(#softGlow)"/><path d="M786 70 C728 96 729 218 790 244" fill="none" stroke="url(#glass)" stroke-width="55" stroke-linecap="round" opacity=".88"/><path d="M1042 70 C1100 96 1099 218 1038 244" fill="none" stroke="#06231d" stroke-width="74" stroke-linecap="round" filter="url(#softGlow)"/><path d="M1042 70 C1100 96 1099 218 1038 244" fill="none" stroke="url(#glassReverse)" stroke-width="55" stroke-linecap="round" opacity=".88"/><circle cx="913" cy="157" r="47" fill="url(#orb)" filter="url(#smallGlow)"/><path d="M845 157H981" stroke="#eaffff" stroke-width="4" stroke-linecap="round" class="scan"/><circle cx="913" cy="157" r="76" fill="none" stroke="#b8ffe9" stroke-opacity=".22" stroke-dasharray="4 10" class="spin"/></g>"""
    if kind == "dialogue":
        return """<g class="drift-alt"><ellipse cx="914" cy="156" rx="235" ry="130" fill="url(#halo)" opacity=".5"/><path d="M745 99 C745 60 782 44 820 44 H972 C1014 44 1035 68 1035 103 V147 C1035 181 1012 202 974 202 H890 L833 246 L844 202 H808 C768 202 745 180 745 145Z" fill="#06231e" stroke="url(#glass)" stroke-width="30" stroke-linejoin="round" opacity=".86" filter="url(#smallGlow)"/><path d="M786 88H970 M786 122H931 M786 156H900" stroke="#eaffff" stroke-opacity=".5" stroke-width="10" stroke-linecap="round"/><circle cx="1007" cy="73" r="25" fill="url(#orb)"/><circle cx="1000" cy="65" r="5" fill="#fff" opacity=".7"/></g>"""
    return f"""<g class="drift"><ellipse cx="914" cy="156" rx="230" ry="132" fill="url(#halo)" opacity=".55"/><path d="M741 157 C787 58 875 66 914 157 C954 248 1044 254 1090 157 C1041 59 953 66 914 157 C875 249 786 256 741 157Z" fill="none" stroke="#06231e" stroke-width="64" stroke-linecap="round" stroke-linejoin="round" filter="url(#softGlow)"/><path d="M741 157 C787 58 875 66 914 157 C954 248 1044 254 1090 157 C1041 59 953 66 914 157 C875 249 786 256 741 157Z" fill="none" stroke="url(#glass)" stroke-width="43" stroke-linecap="round" stroke-linejoin="round" opacity=".8"/><path d="M754 144 C800 71 871 83 902 154" fill="none" stroke="#efffff" stroke-width="6" stroke-linecap="round" opacity=".42"/><circle cx="741" cy="157" r="21" fill="url(#orb)"/><circle cx="914" cy="157" r="27" fill="url(#orb)"/><circle cx="1090" cy="157" r="21" fill="url(#orb)"/><circle r="7" fill="{P['lime']}" filter="url(#smallGlow)"><animateMotion dur="4.8s" repeatCount="indefinite" path="M741 157 C787 58 875 66 914 157 C954 248 1044 254 1090 157"/></circle></g>"""


def build_projects() -> None:
    width, height = 1200, 310
    for index, (slug, eyebrow, title, description, detail, kind) in enumerate(PROJECTS, start=1):
        body = frame(width, height, f"SELECTED SYSTEM / 0{index}") + f"""
  <text x="54" y="92" fill="{P['aqua']}" font-size="12" font-weight="750" letter-spacing="2.4">{eyebrow}</text>
  <text x="54" y="160" fill="{P['white']}" font-size="56" font-weight="830" letter-spacing="-1.5">{title}</text>
  <text x="56" y="205" fill="{P['white']}" font-size="24">{description}</text>
  <text x="56" y="254" fill="{P['muted']}" font-size="14">{detail}</text>
  <path d="M580 58V252" stroke="#173b33"/>{sculpture(kind)}{grain(width, height)}"""
        write_svg(f"assets/projects/{slug}.svg", width, height, f"{title} — {description}", detail, body)


def build_stack() -> None:
    width, height = 1200, 330
    path = "M-438 0 C-320-58 -208 58 -92 0 S133-58 246 0 S359 58 438 0"
    body = frame(width, height, "SYSTEM LAYERS") + f"""
  <text x="54" y="103" fill="{P['white']}" font-size="31" font-weight="770">One product. Four engineered layers.</text>
  <text x="54" y="139" fill="{P['muted']}" font-size="15">The model is only one component of the system.</text>
  <g transform="translate(585 205)"><ellipse rx="470" ry="70" fill="url(#halo)" opacity=".45"/><path d="{path}" fill="none" stroke="#06231e" stroke-width="62" stroke-linecap="round" filter="url(#softGlow)"/><path d="{path}" fill="none" stroke="url(#glass)" stroke-width="43" stroke-linecap="round" opacity=".82"/><path d="M-429-7 C-320-51-207 51-93-7 S132-51 245-7 S358 50 428-7" fill="none" stroke="#f0ffff" stroke-width="5" stroke-linecap="round" opacity=".34"/><circle cx="-438" r="25" fill="url(#orb)"/><circle cx="-92" r="25" fill="url(#orb)"/><circle cx="246" r="25" fill="url(#orb)"/><circle cx="438" r="25" fill="url(#orb)"/><circle r="8" fill="{P['lime']}" filter="url(#smallGlow)"><animateMotion dur="6.5s" repeatCount="indefinite" path="{path}"/></circle></g>
  <g fill="{P['white']}" font-size="13" font-weight="730" text-anchor="middle" letter-spacing="1.4"><text x="147" y="307">EXPERIENCE</text><text x="493" y="307">APPLICATION</text><text x="831" y="307">INTELLIGENCE</text><text x="1023" y="307">INFRASTRUCTURE</text></g>{grain(width, height)}"""
    write_svg("assets/profile/system-layers.svg", width, height, "AI product system layers", "A continuous translucent tube connects experience, application, intelligence, and infrastructure.", body)


def build_social_preview() -> None:
    width, height = 1280, 640
    body = frame(width, height, "ABDULELAH / AI SYSTEMS") + f"""
  <text x="58" y="164" fill="{P['white']}" font-size="72" font-weight="820" letter-spacing="-2">I ENGINEER</text><text x="58" y="250" fill="url(#glass)" font-size="92" font-weight="880" letter-spacing="-3">AI SYSTEMS</text><text x="62" y="307" fill="{P['muted']}" font-size="23" letter-spacing="2.8">THAT THINK  ·  ACT  ·  EARN TRUST</text><text x="62" y="390" fill="{P['white']}" font-size="22">AI Agents  /  Voice AI  /  RAG  /  Product Engineering</text><text x="62" y="558" fill="{P['muted']}" font-size="16" letter-spacing="2">ABDULELAH.DE</text>
  <g class="drift" transform="translate(970 310)"><ellipse rx="235" ry="220" fill="url(#halo)" opacity=".8"/><path d="M-120 100 C-188 4-122-126-10-130 C95-134 164-30 123 67 C93 138-17 147-62 76 C-92 28-60-35-5-30 C47-25 60 38 23 65" fill="none" stroke="#05251e" stroke-width="104" stroke-linecap="round" filter="url(#softGlow)"/><path d="M-120 100 C-188 4-122-126-10-130 C95-134 164-30 123 67 C93 138-17 147-62 76 C-92 28-60-35-5-30 C47-25 60 38 23 65" fill="none" stroke="url(#glass)" stroke-width="78" stroke-linecap="round" opacity=".88"/><path d="M-127 89 C-183 0-119-113-14-117 C84-121 148-26 111 58" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".34"/><circle cx="-120" cy="100" r="49" fill="url(#orb)"/></g>"""
    write_svg("assets/profile/social-preview.svg", width, height, "Abdulelah Alkhathami — AI systems", "I engineer AI systems that think, act, and earn trust.", body)


def main() -> None:
    build_hero(); build_flow(); build_projects(); build_stack(); build_social_preview()
    print("Generated 7 retro-futuristic profile assets.")


if __name__ == "__main__":
    main()
