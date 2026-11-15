# Signature Terminal

The one visual language for this GitHub account: the profile and every project
open with the same terminal window, and each project shows one motion of its own.

Source of truth: [`tools/terminal_system.py`](../tools/terminal_system.py) (the
system) and [`tools/build_terminal.py`](../tools/build_terminal.py) (the scenes).
Never hand-edit a generated SVG.

## Principles

- **Restraint.** One window, one typeface, one accent. No badges, stats, glow or gradients.
- **Truth.** Every value on screen comes from the project: captured evidence, its own
  data, or its own rules run on a stated input. Sample inputs say so inside the hero.
- **Still is finished.** The resting style of every element is its final state, so a
  reader with reduced motion, or a renderer without CSS animation, sees the whole frame.
- **Once.** Motion plays a single time in about four to six seconds. Only the last cursor blinks.

## Palette

| Token | Value | Use |
|---|---|---|
| Background | `#0E0F11` | Window. Dark on both GitHub themes: an object on light, a quiet panel on dark |
| Edge / rule | `#26292E` / `#1B1E22` | Window border and title-bar rule |
| Ink / name | `#E9E6DF` / `#F4F1EB` | Commands, output, names |
| Muted / faint | `#8F9299` / `#62676E` | Purpose lines, labels, status, comments |
| Separator / track | `#5A5E65` / `#1C1F23` | Dividers, meter and bar tracks |
| Accent (sand) | `#C9A86C` | `$`, cursors and each project's single highlight. Nothing else |

## Type

- **Geist Mono** (The Geist Project Authors, SIL OFL 1.1), embedded per file as a WOFF2
  subset of the glyphs on screen, because GitHub's image sandbox blocks remote fonts.
  Regular for everything; Light 300 for names.
- **IBM Plex Sans Arabic** Light (IBM Corp., SIL OFL 1.1), shaped with HarfBuzz and
  drawn as outlines, so Arabic renders identically everywhere without bidi surprises.
- Fonts come from pinned npm packages through jsDelivr and are checked against SHA-256.

## Window

Rounded window with three neutral dots and the title `abdulelah@github`. The profile
is home: its prompt is `~ $`. Each project is a folder: `~/raqmi $` on wide screens; on
phones the path moves to the title bar and the prompt is `$`.

Project heroes open with the name (Light 300), a purpose line, and an honest status
tag. Then one command types itself and its output carries the project's motion.

## Motion

| Repository | Purpose line | Signature motion |
|---|---|---|
| Profile | Applied AI Engineer | `whoami` reveals the name and its Arabic form |
| Raqmi | Authorized AI actions | The denied tool call is struck through; allowed calls light up |
| ChatUB | Arabic local intelligence | The Arabic question types itself right to left |
| Abdulelah.de | Verified AI portfolio | `uniq -c` tallies the portfolio's status counts |
| Althil | Solar and shade intelligence | The sun climbs its arc to the computed altitude |
| Absher Insight | Explainable risk signals | Risk meters fill to the rule-assigned probability |
| Stadium | Computer vision monitoring | Gate bars rise; one crosses 80% and flips to OVERFLOW |

Shared: character-by-character typing with a human rhythm, a 2 px sand cursor that
travels with the text, soft 5 px rises for output, and a slow blink once at rest.

## Responsive and themes

Every hero ships as `assets/terminal.svg` (880 wide) and `assets/terminal-mobile.svg`
(390 wide). READMEs swap them with `<picture>` and `(max-width: 600px)`, because an
SVG inside `<img>` cannot reflow. The dark window reads correctly on GitHub's light
and dark themes, so no theme variants are needed.

## README structure

Every project README follows the same order:

1. Hero, linked back to the profile
2. One sentence on what it is, then an honest status line
3. `###### HOW IT WORKS`: four or five steps
4. `###### EVIDENCE`: what is verified, then what is not claimed
5. `###### QUICK START`
6. `###### DOCUMENTATION`, including the full overview the README used to hold

The small uppercase `######` labels match the profile's `SELECTED WORK` and `CONNECT`.

## Build

```bash
pip install fonttools brotli uharfbuzz
python tools/build_terminal.py                                    # profile -> assets/
python tools/build_terminal.py raqmi --out ../llm-application-engineering-Raqmi/assets
python tools/build_terminal.py --all --out build                  # every scene
```

Scenes: `profile`, `raqmi`, `chatub`, `abdulelah.de`, `althil`, `absher-insight`,
`stadium`. Two runs give byte-identical files.

## Retired

The previous sculptural identity (cyan–lime 3D artwork, per-repository
`assets/branding/` folders, `tools/build_brand_assets.py`, the generated avatar and
social previews) was removed in November 2026. It remains in each repository's Git
history; the profile's last version of it is commit `2223e4f`.
