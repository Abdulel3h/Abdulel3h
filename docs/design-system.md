# Permission Moment · design system

The paired-line gate is an original mark for the gap between model intent and application authority. It appears as an abstract mark in the hero, a pause in the trace and a bounded path for Raqmi. The portfolio uses two conversation windows; ChatUB aligns retrieval inputs; Absher Insight uses synthetic signal cells; Stadium uses gate arcs. Shared spacing and typography create a family without repeating one diagram.

| Token | Light | Dark |
|---|---|---|
| Canvas | `#f4f2ea` | `#101310` |
| Ink | `#20251e` | `#f2f1e8` |
| Secondary | `#535b4b` | `#b3bbaa` |
| Boundary | `#435c18` | `#d4e896` |

Arial / Helvetica / sans-serif; no remote fonts, textures, models or widgets. All assets have explicit backgrounds. SVG title/description and HTML alt text preserve the message. Essential state uses words and geometry as well as color.

Desktop hero: 800 × 224; trace: 800 × 222; cards: 800 × 152. Mobile artwork: 400 × 156, 400 × 184 and 400 × 136, selected with native picture media sources. A browser preference selects light/dark artwork. If the user's GitHub theme differs from the browser preference, each SVG remains readable on its own opaque canvas. Fallback is the light desktop image. At 320px outer width with 16px side padding, the mobile hero headline is about 29px and project value text about 14px. Secondary category labels are smaller and are repeated in meaningful alt text.

One 4.6-second animation plays once and stops. A moving signal pauses at the gate; the complete labeled diagram exists from the first frame. `prefers-reduced-motion: reduce` disables animation. No essential text appears only transiently. No JavaScript or workflow is installed in the profile. The denied path is an actual GitHub details/summary disclosure, not an embedded SVG click handler. The illustration is not a running agent, fake terminal or live-data display.

Rebuild SVGs: `python tools/build_profile.py`. Rebuild PNG social assets: `node tools/render_social.cjs` with `sharp` available. SVGs remain editable text/vector sources; social PNGs bake the final rendering. Do not add confidential audit notes to this repository.
