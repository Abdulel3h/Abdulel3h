# GitHub settings

What was applied automatically, and exactly what still needs a person.

## Applied and verified

Repository **About descriptions** and **topics** for all six public
repositories were applied through the GitHub API and verified by reading them
back. See [github-presence-map.md](github-presence-map.md) for the per-repository
state.

## Still manual

GitHub exposes no API for the four settings below — a token cannot apply them,
whatever its scopes. Each asset is committed and ready to upload.

### 1. Profile avatar

**File:** [`assets/profile/avatar.png`](../assets/profile/avatar.png) — 1024 × 1024,
under 1 MB, composed for a circular crop and legible at 32px.
Preview at four sizes: [`assets/profile/avatar-preview.png`](../assets/profile/avatar-preview.png).
Editable master: [`assets/profile/avatar.svg`](../assets/profile/avatar.svg).

**Where:** [github.com/settings/profile](https://github.com/settings/profile) →
profile picture → **Edit** → **Upload a photo…** → choose `avatar.png` → keep the
default circular crop → **Set new profile picture**.

### 2. Profile bio

**Where:** [github.com/settings/profile](https://github.com/settings/profile) → **Bio**.

**Value** (96 characters, inside GitHub's 160 limit):

```
AI Systems & Product Engineer | AI Agents · Voice AI · RAG | Arabic-first, accountable by design
```

Leave **Name** (`Abdulelah Alkhathami`), **Website** (`https://abdulelah.de`) and
**Location** (`Riyadh, Saudi Arabia`) as they are.

### 3. Pinned repositories

**Where:** [github.com/Abdulel3h](https://github.com/Abdulel3h) →
**Customize your pins**.

Select exactly these five, in this order:

1. `llm-application-engineering-Raqmi`
2. `Abdulelah`
3. `ChatUB`
4. `absher-insight`
5. `Stadium`

Leave the sixth slot empty. Do **not** pin `Abdulel3h` — the profile README is
already the page the visitor is looking at, so pinning it wastes the strongest
slot.

GitHub's pin dialog does not preserve click order in every case; after saving,
open the profile logged out and confirm Raqmi appears first.

### 4. Social previews

For each repository: **Settings → General → Social preview → Edit → Upload an
image**. All are 1280 × 640 and under 1 MB.

| Repository | File |
|---|---|
| [Abdulel3h](https://github.com/Abdulel3h/Abdulel3h/settings) | [`assets/profile/social-preview.png`](../assets/profile/social-preview.png) |
| [llm-application-engineering-Raqmi](https://github.com/Abdulel3h/llm-application-engineering-Raqmi/settings) | `assets/branding/social-preview.png` |
| [Abdulelah](https://github.com/Abdulel3h/Abdulelah/settings) | `assets/branding/social-preview.png` |
| [ChatUB](https://github.com/Abdulel3h/ChatUB/settings) | `assets/branding/social-preview.png` |
| [absher-insight](https://github.com/Abdulel3h/absher-insight/settings) | `assets/branding/social-preview.png` |
| [Stadium](https://github.com/Abdulel3h/Stadium/settings) | `assets/branding/social-preview.png` |

## Why these are manual

The REST API has no endpoint for the avatar, the pinned-repository list or the
social preview image. Changing the bio needs a token with the `user` scope; the
credential available here carries `gist, repo, workflow`, which is why
descriptions and topics could be applied and the bio could not.

No Actions or workflows are required: the artwork is self-contained SVG with no
scripts, remote fonts or external services.
