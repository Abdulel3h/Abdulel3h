# GitHub settings · apply after design approval

This branch changes presentation files only. Global profile/repository settings remain a manual review step. The connected tools available in this session do not expose setters for bio, pins, About/topics or social-preview images. Do not merge or apply these settings merely to inspect the branch.

## Profile

- Name: `Abdulelah Alkhathami`
- Bio: `AI Product Builder · Arabic-first systems · Bounded tools, evaluation & thoughtful UX.`
- Website: `https://abdulelah.de`
- Public contact: `me@abdulelah.de`
- LinkedIn: `https://linkedin.com/in/abdulelah-alkhathami-853845311`
- Location: keep the existing public location; no location change is necessary.

Use profile → **Edit profile** for name, bio, website and public links. Keep email visibility intentional; the README uses the already-public contact address.

## Exact pin order

Profile → **Customize your pins** → select the public repositories below → **Save pins**; drag the handles to this order.

| Slot | Repository | Reason |
|---|---|---|
| 1 | `llm-application-engineering-Raqmi` | Strongest inspectable AI-system evidence |
| 2 | `Abdulelah` | Product interface and bilingual assistant |
| 3 | `ChatUB` | Arabic local-LLM prototype |
| 4 | `absher-insight` | Backend and synthetic analytics breadth |
| 5 | `Stadium` | Computer-vision system concept |
| 6 | `Abdulel3h` | Optional: original GitHub-native design artifact after this branch is approved |

There are five public project repositories, so slot six is explicitly the profile artifact, not an invented sixth AI product. Leave it empty if you want projects only. The custom README features only the first three.

## About, topics and repository first screens

For each repository: open its **Code** page → gear next to **About** → enter the values below → **Save changes**. Keep the repository names/URLs stable. Display names can be human-readable without renaming repos.

| Repository | Final About description | Topics | Homepage |
|---|---|---|---|
| `llm-application-engineering-Raqmi` | Arabic-first retail AI study with native tool calling, application-owned authorization, explicit consent, and evaluation. | `arabic-nlp`, `llm-applications`, `tool-calling`, `authorization`, `guardrails`, `evaluation`, `pydantic` | Leave blank until a dedicated public project page is verified. |
| `Abdulelah` | Bilingual AI-builder portfolio with case studies and an embedded assistant, built with Next.js and TypeScript. | `portfolio`, `arabic`, `ai-assistant`, `nextjs`, `react`, `typescript` | `https://www.abdulelah.de` |
| `ChatUB` | Arabic academic-assistance prototype using FAQ retrieval, multilingual embeddings, Flask, and local Ollama generation. | `arabic-nlp`, `semantic-search`, `ollama`, `flask`, `ai-assistant`, `prototype` | Keep existing public portfolio case-study URL; validate it before changing. |
| `absher-insight` | Independent security-analytics prototype with FastAPI, synthetic events, and behavioral rules. | `fastapi`, `synthetic-data`, `security-analytics`, `dashboard`, `prototype` | Keep existing public portfolio case-study URL; validate it before changing. |
| `Stadium` | Computer-vision gate-monitoring prototype using YOLO, OpenCV, Flask, and frame-level crowd counts. | `computer-vision`, `yolo`, `opencv`, `flask`, `prototype` | Leave blank; no verified standalone deployment. |
| `Abdulel3h` | Abdulelah Alkhathami — AI Product Builder. Arabic-first systems, bounded actions, and thoughtful product UX. | `github-profile`, `ai-products`, `arabic`, `svg`, `portfolio` | `https://abdulelah.de` |

Current-state findings: Raqmi's About/topics/homepage are empty. The other four project descriptions and topics already carry useful positioning, but prototype scope can be clearer; the portfolio's current AI-engineer label can align with the new product-builder identity. Current project README heroes still belong to the previous visual system. Their code/results/README files are untouched by this profile-only branch. After approval, lead each project README with its display name, one value sentence, explicit scope, and a compact source/demo entry; use the matching artwork rather than stacking a giant hero over a repeated paragraph.

## Social-preview uploads

Each PNG is 1280 × 640. Repository → **Settings** → **General** → **Social preview** → **Edit** → **Upload an image** → choose the matching PNG from this branch. This is a repository social preview; it does not replace the GitHub account avatar or create a profile-level social-card setting.

| Repository | File |
|---|---|
| `Abdulel3h` | [profile.png](../assets/social/profile.png) |
| `llm-application-engineering-Raqmi` | [raqmi.png](../assets/social/raqmi.png) |
| `Abdulelah` | [portfolio.png](../assets/social/portfolio.png) |
| `ChatUB` | [chatub.png](../assets/social/chatub.png) |
| `absher-insight` | [absher-insight.png](../assets/social/absher-insight.png) |
| `Stadium` | [stadium.png](../assets/social/stadium.png) |

## Review and eventual activation

Review [the branch README](https://github.com/Abdulel3h/Abdulel3h/blob/design/profile-v2/README.md) and [design report](redesign-report.md). A non-default branch README cannot replace the account homepage. Only after separate approval: merge the reviewed branch into `main`, then apply the UI settings above. No PR merge, force push or default-branch change is part of this delivery.

Primary UI references: [pinning items](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/pinning-items-to-your-profile), [repository social previews](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview).
