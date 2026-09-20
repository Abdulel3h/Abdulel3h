# GitHub brand system

The canonical rules for Abdulelah Alkhathami's public GitHub presence. Every
public repository generates its artwork from these rules, so the account reads
as one system rather than six unrelated projects.

## Purpose

A visitor should be able to tell, within a few seconds and from any repository,
that they are looking at the same engineer's work — and should be able to tell
the projects apart just as quickly. Shared material, distinct silhouettes.

## Palette

| Role | Hex |
|---|---|
| Deep black | `#030706` |
| Frosted white | `#F4FFF9` |
| Cyan | `#46F6FF` |
| Aqua | `#22E3C5` |
| Lime | `#C8FF54` |
| Deep blue | `#3B65FF` |

Supporting tones: surface `#06100E`, hairline border `#123029`, muted text
`#8FA8A1`, dim label `#5E7A74`.

**Lime is reserved.** It marks the travelling signal and the moment of
authorization — never decoration. **The cold white-blue mix (`glassCold`) is
reserved for boundaries**: the authorization monolith, Raqmi's threshold arch,
Stadium's gate. That reservation is what makes "this is the boundary" legible
without a padlock icon.

## Material

Flat geometry is inflated by a lighting filter: the blurred alpha channel
becomes a height field, so any silhouette gains a soft bevel, diffuse shading, a
cyan rim on the shadow side and a controlled specular highlight. Three sizes —
`glossL`, `glossM`, `glossS` — matched to the mass of the form.

- One distant key light: azimuth 228°, elevation 58° (upper left). Never varies.
- Overlapping parts are **separate filtered groups**, so they occlude and refract
  each other instead of merging into one blob.
- Depth: a dim light pool on the floor with the object's occlusion sitting in it.
- Atmosphere: restrained aqua haze behind the hero object, plus a grain pass over
  the whole composition.

## Typography

System fonts only; no webfont is ever fetched.

- Sans: `ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`
- Mono: `ui-monospace, SFMono-Regular, "SF Mono", "Cascadia Mono", "Segoe UI Mono", Consolas, monospace`

Mono carries slugs, eyebrows and status labels; sans carries names and taglines.
Because fallback fonts differ in width, **long names get an explicit smaller size**
rather than being allowed to run into the sculpture. Check any new copy against a
wide fallback (Verdana or DejaVu Sans), not just the local font.

## Motion

Motion describes system behaviour; it never merely decorates.

- **Every animation is CSS.** SMIL is forbidden: no media query can stop it, so it
  keeps repainting even for readers who asked for reduced motion.
- **Two roles.** Identity and system diagrams may loop. Project cards play a single
  activation when first painted, then rest.
- **Stepped timing on a shared grid.** A browser re-rasterises an SVG loaded through
  `<img>` in full on every animation frame, filters included, so a smooth 60fps
  loop costs roughly a core per card. Each asset runs on one duration and one step
  grid; animations on different phases multiply the repaint rate instead of
  sharing it. Intervals where nothing changes collapse to a single step.
- Reference cost, measured in headless Chrome at GitHub's content width with six
  cards on screen: **0.56 of one core with motion, 0.01 with reduced motion.**

Forbidden: bouncing, spinning, flashing, and any motion that harms readability.

## Responsive rules

Every main visual ships a wide variant and a portrait variant, selected in
Markdown with `<picture>` and `media="(max-width: 600px)"` — GitHub preserves both
the media query and relative `srcset` paths.

The portrait variant is **recomposed, not shrunk**: sculpture above, type below,
larger type, shorter supporting copy, safe edge spacing. Check every asset at the
original canvas, ~800px (GitHub's content width), 640px and 360–400px.

## Accessibility

- Every SVG carries `<title>` and `<desc>`.
- Every README image carries meaningful alternative text.
- `prefers-reduced-motion: reduce` stops every animation, hides `.motion` groups
  and reveals `.still` groups. Verify with Chrome's
  `--force-prefers-reduced-motion` flag: page-level emulation (DevTools,
  Playwright) does **not** reach inside an SVG loaded as an image.
- Each card's resting state is the end of its activation, so a reduced-motion
  reader sees the finished story, not an empty stage.
- The first painted frame is always a complete composition. Cards below the fold
  start animating when they are first painted, so an activation brightens a
  finished scene — it never fades one in from nothing.

## Repository asset structure

```text
assets/branding/
├── README.md             How the assets are made and what they mean
├── hero.svg              Wide README hero, 1200 x 360
├── hero-mobile.svg       Portrait README hero, ≤600px viewports
├── cover.svg             Editorial cover, 1280 x 640
├── social-preview.svg    Editable master for the social card
└── social-preview.png    1280 x 640 upload, under 1 MB
tools/build_brand_assets.py
```

The profile repository uses `tools/build_retro_future_profile.py` for the same
purpose and additionally generates the avatar.

## Social previews

1280 × 640, PNG under 1 MB, editable SVG master retained. Composed for a
thumbnail: fewer elements, larger type, one project-specific sculpture, no
unsupported claims. Uploading is a manual step — generating the PNG does not
configure the repository setting.

## Avatar

One luminous sculptural "A" on deep black, sized to survive GitHub's circular
crop and to stay recognisable at 32px. No text, no thin details. Files:
`assets/profile/avatar.svg`, `avatar.png` (1024 × 1024), `avatar-preview.png`
(1024 / 256 / 64 / 32 with circular crop).

## Prohibited

Rainbow gradients · generic purple AI branding · excessive bloom · cheap
glassmorphism · random neon · crowded compositions · stock 3D icons · literal
shields, brains, robots, cameras, chat bubbles or padlocks · contribution snakes
· trophy widgets · badge walls · generic technology icon grids · remote images ·
remote fonts · scripts, event handlers or `foreignObject` inside SVG.

## Update workflow

1. Edit the generator, never the generated SVG.
2. Run the generator twice and confirm byte-identical output.
3. Parse every SVG as XML and render it.
4. Check the wide and portrait variants at 1200/800/640/380px, and against a wide
   fallback font.
5. Scan for scripts, event handlers, remote resources and `foreignObject`.
6. Re-export the social preview PNG and confirm 1280 × 640 and under 1 MB.
7. Commit the generator and the generated assets together.
