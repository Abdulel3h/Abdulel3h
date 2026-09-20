# Sculptural retro-futuristic profile system

The profile is built from one original family of abstract 3D-like SVG sculptures:
inflated tubular geometry, frosted translucent surfaces, a cyan–aqua–lime–blue
gradient family, a single cinematic key light from the upper left, soft contact
shadows and a fine analog grain.

## Source of truth

`tools/build_retro_future_profile.py` generates every asset below. Never hand-edit
the generated SVGs — edit the generator and regenerate:

```
python3 tools/build_retro_future_profile.py
```

The generator has no third-party dependencies and is deterministic: two runs
produce byte-identical files.

| Asset | Wide | Portrait (≤600px) |
|---|---|---|
| Hero | `assets/profile/hero.svg` | `assets/profile/hero-mobile.svg` |
| Accountable agent flow | `assets/profile/system-flow.svg` | `assets/profile/system-flow-mobile.svg` |
| Product layers | `assets/profile/system-layers.svg` | `assets/profile/system-layers-mobile.svg` |
| Raqmi | `assets/projects/raqmi.svg` | `assets/projects/raqmi-mobile.svg` |
| Abdulelah.de | `assets/projects/portfolio.svg` | `assets/projects/portfolio-mobile.svg` |
| ChatUB | `assets/projects/chatub.svg` | `assets/projects/chatub-mobile.svg` |
| Social preview | `assets/profile/social-preview.svg` | — |
| Avatar | `assets/profile/avatar.svg` | — |

The README selects the portrait variants with `<picture>` and a
`(max-width: 600px)` media query, so phone-width readers get type sized for a
phone instead of a scaled-down wide canvas.

### Social preview PNG

GitHub's social preview field takes a raster image. Export it from the SVG master
with headless Chrome (1280 × 640, under 1 MB, no extra dependency):

```
chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --virtual-time-budget=3000 --window-size=1280,640 \
  --screenshot=assets/profile/social-preview.png \
  file://$PWD/assets/profile/social-preview.svg
```

## Material

Every form is drawn as flat geometry and inflated by a lighting filter: the
blurred alpha channel becomes a height field, so any silhouette gains a soft
bevel, diffuse shading, a cyan rim on the shadow side and a controlled specular
highlight. Three sizes exist — `glossL`, `glossM`, `glossS` — matched to the mass
of the form. Overlapping parts are separate filtered groups, so they occlude and
refract each other instead of merging into one blob.

- Light: one distant key light, azimuth 228°, elevation 58° (upper left).
- Depth: a dim light pool on the floor with the object's occlusion sitting in it.
- Atmosphere: restrained aqua haze behind each hero object, plus a grain pass over
  the whole composition.

## Palette

| Role | Hex |
|---|---|
| Deep black | `#030706` |
| Frosted white | `#F4FFF9` |
| Cyan | `#46F6FF` |
| Aqua | `#22E3C5` |
| Lime | `#C8FF54` |
| Deep blue | `#3B65FF` |

Lime is reserved for the travelling signal and for authorization moments. The
cold white–blue mix (`glassCold`) is reserved for boundaries: the authorization
monolith and Raqmi's threshold arch read as denser and colder than the warm
translucent stages around them.

## Typography

System fonts only — no webfont is ever fetched. A sans stack
(`ui-sans-serif, -apple-system, "Segoe UI", Roboto, …`) carries headlines and
labels; a mono stack carries slugs and eyebrows. Type is sized so the smallest
label stays legible at GitHub's ~800px content width, and the portrait variants
re-size type for ~360px phones.

## Motion

Motion describes system behaviour rather than decorating it: the signal halts at
the authorization boundary, the Raqmi payload waits outside the threshold until
it ignites, light cascades down through the four layers, ChatUB's nodes wake in
sequence.

**Every animation is CSS.** SMIL was removed deliberately: no media query can
stop it, so a SMIL timeline keeps running — and keeps the browser repainting —
even for a reader who asked for reduced motion.

**Two motion roles.** The hero and the flow diagram loop on a 12 s cycle,
because the identity and the authorization boundary are what the motion is
*for*. The three project cards and the layer stack instead play a single
activation when they are first painted — which, in a README, is the moment the
reader scrolls to them — and then rest.

**Stepped timing, on a shared grid.** A browser re-rasterises an SVG loaded
through `<img>` in full on every animation frame, lighting filters included, so
a smooth 60 fps loop costs roughly a core per card. Each asset therefore runs on
one duration and one step grid (`LOOP_GRID`, `CARD_GRID`): five animations
stepping on five different phases would cost five times as much as five
animations that land on the same frames. Intervals where nothing changes
collapse to a single step, so a held pose is free.

Measured in headless Chrome at GitHub's content width, all six cards on screen
at once: **0.56 of one core with motion, 0.01 with reduced motion.** Before the
stepped grid the same page cost about 1.4 cores, and reduced motion saved
nothing at all.

- `prefers-reduced-motion: reduce` stops every animation, hides the `.motion`
  groups and reveals the `.still` groups. Verify it with Chrome's
  `--force-prefers-reduced-motion` flag: a page-level emulation (DevTools,
  Playwright) does **not** reach inside an SVG loaded as an image.
- Each card's resting state is the end of its activation, so a reader with
  reduced motion sees the finished story — the payload across the threshold, the
  lattice lit — not an empty stage.
- The un-animated first frame is a complete composition on its own.

## Constraints

No scripts, no event handlers, no `foreignObject`, no remote images, no remote
fonts, no external animation services. Every important claim also exists as
Markdown text outside the artwork, every SVG carries `<title>` and `<desc>`, and
every README image carries alternative text.

Keep new visuals inside this material, lighting, colour and motion language.
Avoid generic technology icons, rainbow gradients, crowded backgrounds, and
motion without narrative purpose.
