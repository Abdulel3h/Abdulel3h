#!/usr/bin/env python3
"""Build the Signature Terminal README heroes for the profile and its projects.

    pip install fonttools brotli uharfbuzz
    python tools/build_terminal.py                     # profile -> assets/
    python tools/build_terminal.py raqmi --out ../llm-application-engineering-Raqmi/assets
    python tools/build_terminal.py --all --out build   # every scene -> build/<scene>/

Each scene writes terminal.svg (wide) and terminal-mobile.svg (phones; READMEs
swap it in below 600px). The design system lives in terminal_system.py.

Every scene shares the window, palette, type, prompt and typing. Each project
has one signature motion of its own:

  profile       whoami reveals the name
  raqmi         a denied tool call is struck through; allowed calls light up
  chatub        an Arabic question types itself right to left
  abdulelah.de  `uniq -c` tallies the portfolio's honest status counts
  althil        the sun climbs its arc to the computed altitude
  absher        risk meters fill to the rule-assigned probability
  stadium       gate bars rise; one crosses 80% and flips to OVERFLOW

Values shown are real: captured evidence (Raqmi), repository data (ChatUB,
Abdulelah.de), the projects' own rules and pysolar output (Althil, Absher,
Stadium). Illustrative inputs are labelled as such inside the hero.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from terminal_system import (  # noqa: E402
    ACCENT, BG, EASE, INK, PHONE, SEP, TRACK, WIDE, Frame, Layout, num,
)

ROOT = Path(__file__).resolve().parents[1]


# ── Profile ─────────────────────────────────────────────────────────────────
NAME, NAME_AR = "Abdulelah Alkhathami", "عبدالإله الخثعمي"
ROLE = "Applied AI Engineer · Riyadh"
FOCUS = ("AI agents", "LLM systems", "Arabic-first AI")


def profile(L: Layout) -> Frame:
    f = Frame(L, f"{NAME} — Applied AI Engineer",
              f"{NAME} ({NAME_AR}), Applied AI Engineer, Riyadh. Focus: {', '.join(FOCUS)}.", size=16)
    p = L.phone
    y = dict(p1=86, name=140, ar=177, role=211, p2=264, focus=(298, 326, 354), p3=408, h=446) if p else \
        dict(p1=92, name=150, ar=150, role=182, p2=236, focus=(268,), p3=318, h=356)
    f.chrome(y["h"])
    enter = f.command(y["p1"], "~", "whoami", .6)
    t_name = enter + .08
    f.text(f.col(0) - L.name_size * .04, y["name"], NAME, "n", f.rise(t_name, .62))
    f.arabic(NAME_AR, 22 if p else 27, L.right, y["ar"], "ar", f.rise(t_name + .18, .62))
    f.text(f.col(0), y["role"], ROLE, "m r", f.rise(t_name + .34, .5))
    p2 = t_name + .86
    enter2 = f.command(y["p2"], "~", "cat focus", p2 + .34, prompt_at=p2)
    times = [enter2 + .08 + .13 * i for i in range(3)]
    if p:
        for item, yy, t in zip(FOCUS, y["focus"], times):
            f.text(f.col(0), yy, item, "m", f.rise(t, .5))
    else:
        c = 0
        for i, (item, t) in enumerate(zip(FOCUS, times)):
            f.add(f"<g{f.rise(t, .5)}>")
            if i:
                f.text(f.col(c + 2), y["focus"][0], "·", "m sep")
                c += 5
            f.text(f.col(c), y["focus"][0], item, "m")
            f.add("</g>")
            c += len(item)
    f.rest(y["p3"], "~", times[-1] + .52)
    return f


# ── Project scenes ──────────────────────────────────────────────────────────
def project(L: Layout, name: str, persona: str, tag: str, path: str, alt: str, height: dict) -> Frame:
    f = Frame(L, f"{name} — {persona}", alt)
    f.chrome(height["phone" if L.phone else "wide"], path)
    if L.phone:
        f.header(name, persona, tag, 92, 118, 142)
    else:
        f.header(name, persona, tag, 100, 130)
    return f


def raqmi(L: Layout) -> Frame:
    path = "~/raqmi"
    f = project(L, "Raqmi", "Authorized AI actions", "case study · fictional data", path,
                "Raqmi, authorized AI actions. Captured live DeepSeek run: lookup_order for order 5521 was "
                "denied by application authorization (authorization_denied); lookup_order for order 1024 and "
                "create_return were allowed and created return R-1001.",
                {"wide": 372, "phone": 440})
    rows = [("lookup_order(order_id=5521)", "denied", "authorization_denied"),
            ("lookup_order(order_id=1024)", "allowed", ""),
            ("create_return(order_id=1024, …)", "allowed", "R-1001")]
    f.rule(f"@keyframes struck{{from{{fill:{INK}}}}}"
           "@keyframes draw{from{stroke-dashoffset:1}}")
    enter = f.command(186, path, "# captured live run", .5)
    t = enter + .1
    for i, (call, verdict, detail) in enumerate(rows):
        if L.phone:
            y, yv, cv, cd = 220 + i * 58, 244 + i * 58, 2, 10
        else:
            y, yv, cv, cd = 222 + i * 32, 222 + i * 32, 36, 45
        denied = verdict == "denied"
        t_verdict = t + .55
        cls = "m dim" if denied else "m"
        style = f.rise(t, .45) if not denied else \
            f' style="{f.anim("up", .45, t, EASE)},struck .5s ease {num(t_verdict + .1)}s both"'
        f.text(f.col(0), y, call, cls, style)
        f.text(f.col(cv), yv, verdict, "m mut" if denied else "m acc", f.rise(t_verdict, .35))
        if detail:
            f.text(f.col(cd), yv, detail, "m dim" if denied else "m mut", f.rise(t_verdict + .1, .35))
        if denied:
            x1, x2 = f.col(0) - 2, f.col(len(call)) + 2
            f.add(f'<path d="M{num(x1)} {num(y - f.L.size * .3)}H{num(x2)}" stroke="{SEP}" stroke-width="1.5" '
                  f'pathLength="1" stroke-dasharray="1" '
                  f'style="{f.anim("draw", .45, t_verdict + .1, "cubic-bezier(.6,0,.2,1)")}"/>')
        t += .78
    f.rest(404 if L.phone else 336, path, t + .25)
    return f


CHATUB_Q = "ما الجهة المسؤولة عن التحويل الداخلي؟"
CHATUB_A = "عمادة القبول والتسجيل"


def chatub(L: Layout) -> Frame:
    path = "~/chatub"
    f = project(L, "ChatUB", "Arabic local intelligence", "prototype", path,
                f"ChatUB, Arabic local intelligence. A question asks which office handles internal transfer "
                f"({CHATUB_Q}); the nearest FAQ entry in data/faq2.json gives the context ({CHATUB_A}); the "
                f"answer is generated by the chatub model through Ollama on the same machine.",
                {"wide": 372, "phone": 434})
    p = L.phone
    enter = f.command(186, path, "curl -s :5000/ask --json @q.json", .5, pace=.5)
    ar = 19 if p else 21
    ys = dict(ql=222, q=252, cl=288, c=318, m=354, rest=398) if p else \
        dict(ql=222, q=222, cl=256, c=256, m=290, rest=336)
    t0 = enter + .15
    f.text(f.col(0), ys["ql"], "question", "m dim", f.appear(t0))
    # The Arabic question types itself right to left. The cover and caret are passing
    # states, so their resting style is the finished frame (WebKit ignores held end keyframes).
    left, stops = f.arabic(CHATUB_Q, ar, L.right, ys["q"], "ink", "")
    width = L.right - left
    times = [t0 + .2 + .055 * i for i in range(len(stops))]
    cover = "".join(f"{num((t - t0) / (times[-1] + .2 - t0) * 100)}%{{transform:scaleX({num((s - left + .5) / width)})}}"
                    for s, t in zip(stops, times))
    total = times[-1] + .2
    f.rule(f"@keyframes rtl{{0%{{transform:scaleX(1)}}{cover}100%{{transform:scaleX(0)}}}}")
    caret = "".join(f"{num((t - t0) / (total - t0) * 100)}%{{opacity:1;transform:translateX({num(s - L.right)}px)}}"
                    for s, t in zip(stops, times))
    f.rule(f"@keyframes caret{{0%{{opacity:1;transform:none}}{caret}100%{{opacity:0;transform:translateX({num(left - L.right)}px)}}}}")
    top = ys["q"] - ar * 1.05
    f.add(f'<rect x="{num(left - 3)}" y="{num(top)}" width="{num(width + 6)}" height="{num(ar * 1.5)}" fill="{BG}" '
          f'style="transform:scaleX(0);transform-box:fill-box;transform-origin:left;'
          f'{f.anim("rtl", total - t0, t0, "steps(1,end)", fill="backwards")}"/>')
    f.add(f'<rect x="{num(L.right + 2)}" y="{num(ys["q"] - L.size * .9)}" width="2" height="{num(L.size * 1.2)}" rx="1" '
          f'fill="{ACCENT}" style="opacity:0;{f.anim("caret", total - t0, t0, "steps(1,end)", fill="none")}"/>')
    t1 = total + .25
    if p:
        f.text(f.col(0), ys["cl"], "context · data/faq2.json", "m dim", f.appear(t1))
    else:
        f.text(f.col(0), ys["cl"], "context", "m dim", f.appear(t1))
        f.text(f.col(10), ys["cl"], "data/faq2.json", "m mut", f.appear(t1))
    f.arabic(CHATUB_A, ar, L.right, ys["c"], "ink", f.rise(t1 + .12, .5))
    t2 = t1 + .45
    if p:
        f.text(f.col(0), ys["m"], "model · chatub via Ollama, local", "m dim", f.rise(t2, .45))
    else:
        f.text(f.col(0), ys["m"], "model", "m dim", f.rise(t2, .45))
        f.text(f.col(10), ys["m"], "chatub via Ollama · on this machine", "m mut", f.rise(t2, .45))
    f.rest(ys["rest"], path, t2 + .45)
    return f


STATUS_COUNTS = [("concept", 3), ("graduation-project", 1), ("hackathon-prototype", 2), ("working-prototype", 2)]


def portfolio(L: Layout) -> Frame:
    path = "~/abdulelah.de"
    f = project(L, "Abdulelah.de", "Verified AI portfolio", "deployed · abdulelah.de", path,
                "Abdulelah.de, verified AI portfolio. Counting the status field in data/projects.ts gives "
                "3 concept, 1 graduation-project, 2 hackathon-prototype and 2 working-prototype. The pages "
                "and the assistant read this one file.",
                {"wide": 420, "phone": 436})
    p = L.phone
    cmd = "grep -oE 'status: \"[a-z-]+\"' data/projects.ts | sort | uniq -c"
    if p:
        enter = f.command(186, path, "grep -oE 'status: \"[a-z-]+\"' \\", .5, pace=.4,
                          wrap="data/projects.ts | sort | uniq -c", y_wrap=212)
        y0, step, y_note, y_rest = 248, 26, 358, 400
    else:
        enter = f.command(186, path, cmd, .5, pace=.38)
        y0, step, y_note, y_rest = 222, 28, 340, 384
    t = enter + .12
    for i, (status, count) in enumerate(STATUS_COUNTS):
        y = y0 + i * step
        f.text(f.col(8), y, f'status: "{status}"', "m", f.rise(t, .35))
        # uniq -c tallies: each count steps up to its total.
        for k in range(1, count + 1):
            tk = t + .05 + .22 * (k - 1)
            if k < count:
                f.text(f.col(6), y, str(k), "m acc", f.window(tk, tk + .22))
            else:
                f.text(f.col(6), y, str(k), "m acc", f.appear(tk))
        t += .16
    t_end = t + .22 * 2 + .2
    f.text(f.col(0), y_note, "# pages + assistant read this file" if p else
           "# the pages and the assistant read this one file", "m dim", f.rise(t_end, .5))
    f.rest(y_rest, path, t_end + .55)
    return f


def althil(L: Layout) -> Frame:
    path = "~/althil"
    # Real values: pysolar + Althil's own rules for Riyadh, 15 Jul 2026, 12:00 (UTC+3).
    alt, az, heat, risk = 86.77, 182.98, 66.0, "Moderate"
    f = project(L, "Althil", "Solar and shade intelligence", "hackathon prototype", path,
                f"Althil, solar and shade intelligence. Analysing Riyadh (24.7136, 46.6753) at 12:00 on "
                f"15 July 2026: sun altitude {alt:.1f} degrees, azimuth {az:.1f} degrees, heat score {heat} of 100 "
                f"({risk}), recommended shade: Horizontal Canopy Structure.",
                {"wide": 394, "phone": 504})
    p = L.phone
    if p:
        enter = f.command(186, path, "curl -s :8000/analyze --json \\", .5, pace=.42,
                          wrap="'{\"lat\":24.7136,\"lng\":46.6753}'", y_wrap=212)
        ys = dict(sun=250, heat=276, shade=302, note=328, rest=468)
        rows = [("sun", f"alt {alt:.1f}° · az {az:.1f}°"), ("heat", f"{heat}/100 · {risk}"),
                ("shade", "Horizontal Canopy Structure")]
        c1, cx, cy, r = 6, L.width / 2, 420, 62
    else:
        enter = f.command(186, path, "curl -s :8000/analyze --json '{\"lat\":24.7136,\"lng\":46.6753}'", .5, pace=.4)
        ys = dict(sun=222, heat=252, shade=282, note=314, rest=358)
        rows = [("sun", f"altitude {alt:.1f}°   azimuth {az:.1f}°"), ("heat", f"{heat} / 100 · {risk}"),
                ("shade", "Horizontal Canopy Structure")]
        c1, cx, cy, r = 8, 756, 296, 66
    t = enter + .12
    f.text(f.col(0), ys["sun"], rows[0][0], "m dim", f.rise(t, .4))
    f.text(f.col(c1), ys["sun"], rows[0][1], "m", f.rise(t, .4))
    # The sun climbs its arc from the eastern horizon to the computed altitude.
    angle = 180 - alt if az > 180 else alt
    t_sun, d_sun = t + .2, 1.4
    f.add(f'<path d="M{num(cx - r)} {num(cy)}A{num(r)} {num(r)} 0 0 1 {num(cx + r)} {num(cy)}" fill="none" '
          f'stroke="{TRACK}" stroke-width="1.5"/>')
    f.add(f'<path d="M{num(cx - r - 12)} {num(cy + .5)}H{num(cx + r + 12)}" stroke="{SEP}" stroke-width="1"/>')
    f.text(cx - r, cy + 18, "E", "m dim s", anchor="middle")
    f.text(cx + r, cy + 18, "W", "m dim s", anchor="middle")
    f.add(f'<path d="M{num(cx - r)} {num(cy)}A{num(r)} {num(r)} 0 0 1 {num(cx - r * math.cos(math.radians(angle)))} '
          f'{num(cy - r * math.sin(math.radians(angle)))}" fill="none" stroke="{ACCENT}" '
          f'stroke-width="1.5" stroke-opacity=".45" pathLength="1" stroke-dasharray="1" '
          f'style="{f.anim("draw", d_sun, t_sun, "cubic-bezier(.45,0,.25,1)")}"/>')
    f.rule("@keyframes draw{from{stroke-dashoffset:1}}"
           f"@keyframes climb{{from{{transform:rotate(0deg)}}to{{transform:rotate({num(angle)}deg)}}}}")
    f.add(f'<g style="transform:rotate({num(angle)}deg);transform-origin:{num(cx)}px {num(cy)}px;'
          f'{f.anim("climb", d_sun, t_sun, "cubic-bezier(.45,0,.25,1)")}">'
          f'<circle cx="{num(cx - r)}" cy="{num(cy)}" r="5" fill="{ACCENT}"/></g>')
    t2 = t_sun + d_sun - .35
    f.text(f.col(0), ys["heat"], rows[1][0], "m dim", f.rise(t2, .4))
    f.text(f.col(c1), ys["heat"], rows[1][1], "m", f.rise(t2, .4))
    f.text(f.col(0), ys["shade"], rows[2][0], "m dim", f.rise(t2 + .3, .4))
    f.text(f.col(c1), ys["shade"], rows[2][1], "m acc", f.rise(t2 + .3, .4))
    f.text(f.col(0), ys["note"], "# Riyadh · 15 Jul 2026 · 12:00" if p else
           "# Riyadh, 15 Jul 2026, 12:00 · the API reads the current time", "m dim", f.rise(t2 + .6, .5))
    f.rest(ys["rest"], path, t2 + .9)
    return f


EVENTS = [("Riyadh", "10:15", 2, "Normal", .10, ""),
          ("Jeddah", "03:20", 4, "Suspicious", .85, "Behavior anomaly"),
          ("London", "14:05", 3, "Suspicious", .95, "Location mismatch")]


def absher(L: Layout) -> Frame:
    path = "~/absher-insight"
    f = project(L, "Absher Insight", "Explainable risk signals", "prototype · synthetic data", path,
                "Absher Insight, explainable risk signals. Three synthetic events scored by the /predict rules: "
                "Riyadh 10:15 with 2 actions is Normal (0.10); Jeddah 03:20 with 4 actions is Suspicious (0.85, "
                "behavior anomaly); London 14:05 with 3 actions is Suspicious (0.95, location mismatch). "
                "Not affiliated with Absher or any government entity.",
                {"wide": 394, "phone": 512})
    p = L.phone
    f.rule("@keyframes fill{from{transform:scaleX(0)}}")
    if p:
        enter = f.command(186, path, "for e in a b c; do curl -s \\", .5, pace=.42,
                          wrap=":8000/predict --json @$e.json; done", y_wrap=212)
        meter_w, y0 = 72, 250
    else:
        enter = f.command(186, path, "for e in a b c; do curl -s :8000/predict --json @$e.json; done", .5, pace=.38)
        meter_w, y0 = 120, 252
        f.text(f.col(0), 222, "event", "m dim s", f.appear(enter + .1))
        f.text(f.col(27), 222, "prediction", "m dim s", f.appear(enter + .1))
        f.text(f.col(39), 222, "probability", "m dim s", f.appear(enter + .1))
        f.text(f.col(59), 222, "reason", "m dim s", f.appear(enter + .1))
    t = enter + .3
    y = y0
    for loc, time, actions, pred, prob, reason in EVENTS:
        sus = pred == "Suspicious"
        if p:
            f.text(f.col(0), y, f"{loc}  {time}  {actions} actions", "m", f.rise(t, .35))
            ym, xm, xp = y + 24, f.col(0), f.col(0) + meter_w + 12
        else:
            f.text(f.col(0), y, loc, "m", f.rise(t, .35))
            f.text(f.col(9), y, time, "m mut", f.rise(t, .35))
            f.text(f.col(16), y, f"{actions} actions", "m mut", f.rise(t, .35))
            f.text(f.col(27), y, pred, "m acc" if sus else "m mut", f.rise(t + .1, .35))
            ym, xm, xp = y, f.col(39), f.col(39) + meter_w + 12
        # The meter fills to the rule-assigned probability.
        f.add(f'<rect x="{num(xm)}" y="{num(ym - 9)}" width="{meter_w}" height="6" rx="3" fill="{TRACK}"/>')
        f.add(f'<rect x="{num(xm)}" y="{num(ym - 9)}" width="{num(meter_w * prob)}" height="6" rx="3" '
              f'fill="{ACCENT if sus else SEP}" style="transform-box:fill-box;transform-origin:left;'
              f'{f.anim("fill", .8, t + .2, EASE)}"/>')
        f.text(xp, ym, f"{prob:.2f}", "m", f.appear(t + .95))
        if p:
            f.text(xp + 5 * f.adv, ym, pred, "m acc" if sus else "m mut", f.appear(t + .95))
            if reason:
                f.text(f.col(0), ym + 24, reason, "m dim", f.rise(t + 1.05, .35))
            y += 82 if reason else 58
        else:
            if reason:
                f.text(f.col(59), y, reason, "m dim", f.rise(t + 1.05, .35))
            y += 30
        t += .5
    f.rest(476 if p else 358, path, t + .45)
    return f


GATES = [("A", 18, "NORMAL"), ("B", 33, "BUSY"), ("C", 51, "OVERFLOW"), ("D", 27, "NORMAL")]


def stadium(L: Layout) -> Frame:
    path = "~/stadium"
    f = project(L, "Stadium", "Computer vision monitoring", "prototype", path,
                "Stadium, computer vision monitoring. Sample gate state from /api/status: gate A 18 of 60 "
                "(normal), B 33 of 60 (busy), C 51 of 60 (overflow, past the 80 percent threshold), D 27 of 60 "
                "(normal). Alert: Gate C is 85% full, redirect to gate A.",
                {"wide": 414, "phone": 496})
    p = L.phone
    f.rule("@keyframes rise{from{transform:scaleY(0)}}")
    enter = f.command(186, path, "curl -s :5000/api/status" if p else "curl -s :5000/api/status  # sample state", .5, pace=.55)
    if p:
        f.text(f.col(0), 212, "# sample state", "m dim", f.appear(enter))
    step = 82 if p else 110
    x0 = f.col(0)
    top, bot = (240, 310) if p else (214, 288)
    h = bot - top
    grow, t0 = 1.3, enter + .2
    # The 80% line is the decision engine's CRITICAL_OCCUPANCY threshold.
    y80 = bot - .8 * h
    f.add(f'<path d="M{num(x0)} {num(y80)}H{num(x0 + step * 3 + 40)}" stroke="{SEP}" stroke-width="1" '
          f'stroke-dasharray="2 4" style="{f.anim("k", .01, t0)}"/>')
    f.text(x0 + step * 3 + 48, y80 + 4, "80%", "m dim s", f.appear(t0))
    for i, (gate, count, status) in enumerate(GATES):
        x = x0 + i * step
        pct = count / 60
        hot = status in ("CRITICAL", "OVERFLOW")
        f.add(f'<rect x="{num(x)}" y="{num(top)}" width="6" height="{num(h)}" rx="3" fill="{TRACK}"/>')
        f.add(f'<rect x="{num(x)}" y="{num(bot - h * pct)}" width="6" height="{num(h * pct)}" rx="3" '
              f'fill="{ACCENT if hot else SEP}" style="transform-box:fill-box;transform-origin:bottom;'
              f'{f.anim("rise", grow * pct / .85, t0, "linear")}"/>')
        yc, ys_ = bot + 24, bot + 46
        f.text(x, yc, gate, "m mut", f.appear(t0))
        f.text(x + 2 * f.adv, yc, f"{count}/60", "m", f.appear(t0 + grow * pct / .85))
        if gate == "C":
            # Status follows occupancy through every band on its way up.
            bands = [("NORMAL", 0), ("BUSY", 50), ("CRITICAL", 75), ("OVERFLOW", 80)]
            for j, (word, lo) in enumerate(bands):
                start = t0 + grow * (lo / 100) / .85
                if j < len(bands) - 1:
                    end = t0 + grow * (bands[j + 1][1] / 100) / .85
                    f.text(x, ys_, word, "m dim s", f.window(start, end))
                else:
                    f.text(x, ys_, word, "m acc s", f.appear(start))
        else:
            f.text(x, ys_, status, "m dim s", f.appear(t0 + grow * pct / .85))
    t_alert = t0 + grow + .3
    if p:
        f.text(x0, 392, "alert", "m dim", f.rise(t_alert, .45))
        f.text(x0 + 7 * f.adv, 392, "Gate C is 85% full", "m", f.rise(t_alert, .45))
        f.text(x0 + 7 * f.adv, 416, "redirect to gate A", "m acc", f.rise(t_alert + .15, .45))
        f.rest(460, path, t_alert + .7)
    else:
        xa = x0 + step * 3 + 120
        f.text(xa, top + 12, "alert", "m dim", f.rise(t_alert, .45))
        f.text(xa, top + 42, "Gate C is 85% full", "m", f.rise(t_alert, .45))
        f.text(xa, top + 70, "redirect to gate A", "m acc", f.rise(t_alert + .15, .45))
        f.rest(378, path, t_alert + .7)
    return f


SCENES = {"profile": profile, "raqmi": raqmi, "chatub": chatub, "abdulelah.de": portfolio,
          "althil": althil, "absher-insight": absher, "stadium": stadium}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("scenes", nargs="*", default=["profile"], help=", ".join(SCENES))
    parser.add_argument("--all", action="store_true", help="build every scene")
    parser.add_argument("--out", type=Path, help="output folder (default: assets/ for the profile)")
    args = parser.parse_args()
    names = list(SCENES) if args.all else args.scenes
    for name in names:
        target = args.out / name if (args.out and args.all) else (args.out or ROOT / "assets")
        target.mkdir(parents=True, exist_ok=True)
        for layout, file in ((WIDE, "terminal.svg"), (PHONE, "terminal-mobile.svg")):
            out = target / file
            out.write_text(SCENES[name](layout).build(), encoding="utf-8", newline="\n")
            print(f"{name:<15} {out.as_posix()}  {out.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
