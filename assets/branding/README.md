# Brand system

A calm product-engineering identity: deep navy surfaces, readable white type, cyan for emphasis, and green only for an explicitly allowed state. Visuals explain a request, a boundary and an outcome. They are original SVG documentation, not screenshots or evidence of deployment.

## Assets

| File | Purpose |
|---|---|
| [tokens.json](tokens.json) | Shared colors, type family and cover dimensions |
| [Profile hero](../profile/hero.svg) | Identity and optional animated request flow |
| [Mission Control](../profile/mission-control.svg) | Illustrative scenario; Markdown contains the working links |
| [How I build](../profile/how-i-build.svg) | Six-step product philosophy |
| [Profile social preview](../profile/social-preview.png) | Ready-to-upload 1280 × 640 PNG |
| [Project covers](../projects/) | Six 1280 × 640 SVG covers; copies live in each project's branding folder |

## Use and maintenance

Edit the SVG source directly. Keep each project's cover and its copy in this repository synchronized, then regenerate the project's PNG at 1280 × 640 with an SVG renderer such as Inkscape. Do not rasterize the README asset; the PNG is for GitHub Social Preview.

Use a single full-width image per row in Markdown. Cards stack on mobile. Main names and promises remain text, and important content is repeated in Markdown for assistive technology and image failures. Covers retain the same dark surface in both GitHub themes.

SVGs use system fonts, local shapes, title/description metadata and no remote resources, scripts, embedded images, links or `foreignObject`. Text meaning does not depend on color. The profile hero's optional dashed-line motion shows request direction; CSS `prefers-reduced-motion` stops it where supported, and its static fallback keeps the same information.

The legacy header is retained in history and as an unused file; it is no longer referenced by the profile README. Existing project screenshots are preserved.

[Settings and social-preview mapping](../../docs/github-settings.md) · [Interaction documentation](../../missions/README.md)
