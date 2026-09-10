# GitHub presence redesign

Prepared on 10 September 2026. This report documents presentation changes; commit identities and remote verification are supplied with the delivery response.

## Before and after

| Area | Before | After |
|---|---|---|
| Profile | Long tables, broad stack and links absent from the current public listing; no Raqmi entry | Focused AI Product Builder positioning, bilingual identity, three featured projects and an evidence review path |
| Interaction | None | AI Mission Control: ownership and consent decisions using GitHub Markdown navigation |
| Visuals | Separate project banners | Shared navy/cyan family, six project covers, compact profile and Raqmi heroes, authorization diagram and seven PNG social previews |
| Raqmi | Existing evidence-backed case study already published at `f3abca3e79fa8721e155eca73670d3149b071521` | Refined information architecture, explicit authorization section and diagram; existing results preserved |
| Documentation accuracy | Some stale presentation claims | ChatUB embedding/grounding clarification; Absher CORS and rule-score clarification |

## Profile structure

Hero and links → AI Mission Control → What I build → Featured work → How I build AI → Selected stack → Review/contact links.

## Interaction

[AI Mission Control](../missions/README.md) opens one of three authored outcomes: allow, verify, or escalate. Verification unlocks a second decision about consent. Links are ordinary Markdown, not JavaScript or embedded SVG hotspots. The experience is clearly illustrative and makes no real tool calls. The hero has optional motion with a static fallback.

## Files by repository

### Abdulel3h

- Modified: `README.md`
- Modified: `docs/recruiter-review-path.md`
- Modified: `docs/repository-strategy.md`
- Added: `assets/branding/README.md`
- Added: `assets/branding/tokens.json`
- Added: `assets/profile/hero.svg`
- Added: `assets/profile/how-i-build.svg`
- Added: `assets/profile/mission-control.svg`
- Added: `assets/profile/social-preview.png`
- Added: `assets/projects/absher.svg`
- Added: `assets/projects/architect.svg`
- Added: `assets/projects/chatub.svg`
- Added: `assets/projects/portfolio.svg`
- Added: `assets/projects/raqmi.svg`
- Added: `assets/projects/stadium.svg`
- Added: `docs/github-settings.md`
- Added: `missions/README.md`
- Added: `missions/allow.md`
- Added: `missions/consent-skip.md`
- Added: `missions/consent-verify.md`
- Added: `missions/escalate.md`
- Added: `missions/verify.md`
- Added: `docs/redesign-report.md` (this report).
### llm-application-engineering-Raqmi

- Modified: `README.md`
- Modified: `assets/branding/README.md`
- Modified: `assets/branding/hero.svg`
- Added: `assets/branding/authorization.svg`
- Added: `assets/branding/cover.svg`
- Added: `assets/branding/social-preview.png`
### Abdulelah

- Modified: `README.md`
- Added: `assets/branding/README.md`
- Added: `assets/branding/cover.svg`
- Added: `assets/branding/social-preview.png`
### architect-of-intelligence

- Modified: `README.md`
- Added: `assets/branding/README.md`
- Added: `assets/branding/cover.svg`
- Added: `assets/branding/social-preview.png`
### ChatUB

- Modified: `README.md`
- Added: `assets/branding/README.md`
- Added: `assets/branding/cover.svg`
- Added: `assets/branding/social-preview.png`
### absher-insight

- Modified: `README.md`
- Added: `assets/branding/README.md`
- Added: `assets/branding/cover.svg`
- Added: `assets/branding/social-preview.png`
### Stadium

- Modified: `README.md`
- Added: `assets/branding/README.md`
- Added: `assets/branding/cover.svg`
- Added: `assets/branding/social-preview.png`

## Curation and settings

Recommended pins, in order: **Raqmi, Abdulelah, architect-of-intelligence, ChatUB, absher-insight, Stadium**. See the [audit and exact repository names](repository-strategy.md).

Repository settings changed: **none**. The available tools did not expose those mutations. [Ready-to-paste descriptions, accurate topics and the PNG upload map](github-settings.md) cover the profile and six projects. Pin order, profile bio, About fields and Social Preview uploads require the GitHub UI.

Actions added: **none**. No workflow is needed for Markdown branching or static covers. No existing workflow was modified.

## Validation

- Every changed text file was checked with the existing Raqmi credential-pattern scanner; no detected credential patterns. The Raqmi working-tree scanner also passed. This is a pattern scan, not a guarantee that every possible secret is detectable, and it is not a full-history scan.
- Generated SVGs were parsed and checked for titles/descriptions, scripts, event handlers, external resources, embedded images and oversized payloads. All 17 SVGs rendered to PNG.
- All seven social previews are 1280 × 640 and below 1 MB. SVG source files remain editable.
- Changed Markdown links were checked against local repository paths and heading anchors; GitHub repository/file targets were resolved against the retrieved repositories. External portfolio/LinkedIn availability was not revalidated.
- Representative covers, the profile hero at 320 pixels and the authorization diagram were visually inspected. The actual GitHub desktop/mobile renderer was not available; no live-browser verification is claimed. Plain Markdown duplicates important image content, and the single-column cards scale within GitHub's content width.
- Diff scope is restricted to READMEs, branding assets, profile docs and mission pages. All 25 existing Raqmi files outside its README/branding folder remain byte-identical, including the notebook, implementation, tests, evaluation reports and provenance.
- No application test suite or live model evaluation was rerun for presentation-only changes. Existing reported results retain their captured-evidence labels.

No repository was deleted, renamed, archived, made public or force-pushed as part of this redesign. Existing branch history is preserved with focused presentation commits.
