# GitHub settings

What is applied, and exactly what still needs a person.

## Applied and verified

- Repository **About descriptions** and **topics** for all seven public repositories,
  applied through the GitHub API and read back.
- **Profile bio**, set on 15 November 2026 and read back through the public API:

  ```
  Applied AI Engineer · Arabic-first AI agents and LLM applications
  ```

## Still manual

GitHub has no API for these, whatever a token's scopes.

### 1. Profile photo

**Where:** [github.com/settings/profile](https://github.com/settings/profile) →
profile picture → **Edit** → **Upload a photo…**

The account still shows GitHub's default identicon. A real, recent photo suits the
Signature Terminal identity better than generated artwork, and none is committed
here: the earlier generated avatar was retired with the old identity.

### 2. Pinned repositories

**Where:** [github.com/Abdulel3h](https://github.com/Abdulel3h) → **Customize your pins**.

Select exactly these six, in this order:

1. `llm-application-engineering-Raqmi`
2. `ChatUB`
3. `Abdulelah`
4. `Althil`
5. `absher-insight`
6. `Stadium`

The first three match the profile's selected work. Do **not** pin `Abdulel3h`: the
profile README is already the page the visitor is looking at. Until pins are saved,
GitHub shows its automatic "Popular repositories" list instead.

GitHub's pin dialog does not preserve click order in every case; after saving, open
the profile signed out and confirm Raqmi appears first.

### Social previews (optional)

Every repository currently uses GitHub's generated preview, verified on
15 November 2026. No custom previews are prepared in the new identity; the old
ones were retired, unused, with the previous artwork.

## Why these are manual

The REST API has no endpoint for the profile photo, the pinned-repository list or
the social preview image.

No Actions or workflows are required: every hero is a self-contained SVG with no
scripts, remote fonts or external services.
