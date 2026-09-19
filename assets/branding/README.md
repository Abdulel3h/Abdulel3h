# Retro-futuristic profile system

The profile uses an original family of abstract 3D-like SVG sculptures: inflated tubular geometry, frosted translucent surfaces, cyan–teal–lime gradients, internal glow, deep black fields, and a fine analog grain layer.

## Source and generated assets

Run `python3 tools/build_retro_future_profile.py` from the repository root to regenerate:

- `assets/profile/hero.svg`
- `assets/profile/system-flow.svg`
- `assets/profile/system-layers.svg`
- `assets/profile/social-preview.svg`
- `assets/projects/raqmi.svg`
- `assets/projects/portfolio.svg`
- `assets/projects/chatub.svg`

The generator has no third-party dependencies. Artwork uses no scripts, remote fonts, external images, or `foreignObject` elements. Important claims remain available as Markdown text outside the images.

## Motion and accessibility

Motion communicates system behavior: signals travel through a decision path, not as decoration. CSS and SVG motion stop when `prefers-reduced-motion` is enabled, while the static composition retains its meaning. Every SVG includes a title and description, and every README image has alternative text.

## Palette

| Role | Hex |
|---|---|
| Deep black | `#030706` |
| Frosted white | `#F4FFF9` |
| Cyan | `#46F6FF` |
| Aqua | `#22E3C5` |
| Lime | `#C8FF54` |
| Deep blue | `#3B65FF` |

Keep new visuals within this material, lighting, color, and motion language. Avoid generic technology icons, rainbow gradients, crowded backgrounds, and motion without narrative purpose.
