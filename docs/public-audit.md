# Public work audit

Reviewed all repositories accessible through the connected account, including their current visibility/archive status, tree, README and available implementation/dependency evidence. Empty trees could not provide code evidence. Public claims below use only public sources. There are five public project repositories plus the profile repository; none of this current public set is archived. No visibility or archive settings were changed.

## Curation ranking

Scores are editorial comparisons within this public set, from 1 (weak) to 5 (strong). They are not model benchmarks, seniority ratings or production-readiness certifications. Depth, AI relevance and evidence are weighted twice; other criteria once. Maximum 60. Visual quality means the inspectable product/presentation, not invented user testing.

| Rank | Project | Depth ×2 | Completeness | Originality | Docs | Product value | Visual | AI relevance ×2 | Evidence ×2 | First impression | Total |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Raqmi | 5 | 4 | 4 | 5 | 4 | 3 | 5 | 5 | 4 | 54 |
| 2 | Abdulelah.de | 4 | 4 | 3 | 4 | 4 | 5 | 5 | 4 | 5 | 51 |
| 3 | ChatUB | 3 | 3 | 3 | 3 | 4 | 3 | 5 | 3 | 4 | 42 |
| 4 | Absher Insight | 3 | 3 | 3 | 4 | 3 | 3 | 3 | 3 | 3 | 37 |
| 5 | Stadium | 3 | 3 | 3 | 3 | 4 | 3 | 2 | 3 | 3 | 35 |

### Raqmi — lead with a boundary that can be inspected

Arabic/English retail assistance, structured tools, application-owned authorization and explicit return consent are present in the notebook/tool module. Evaluation artifacts and failure-focused tests make the claims reviewable. The notebook, native tool path and router/model-comparison path are distinct; the homepage does not collapse them into a claim of universal model reliability. It is a capstone/study, not evidence of production customers. [Repository](https://github.com/Abdulel3h/llm-application-engineering-Raqmi), [tool implementation](https://github.com/Abdulel3h/llm-application-engineering-Raqmi/blob/615302c3388ece90c7a94c90c802082dac47f920/raqmi_tool_calling.py), [tests](https://github.com/Abdulel3h/llm-application-engineering-Raqmi/tree/main/tests).

### Abdulelah.de — demonstrate product experience

Next.js/React/TypeScript interface, bilingual content, portfolio-agent modules, server routes and optional model/contact integrations support the product story. Source establishes the intended behavior; this audit does not certify every live integration or any visitor count. It earns second place because it shows how technical work becomes an experience. [Repository](https://github.com/Abdulel3h/Abdulelah), [dependencies](https://github.com/Abdulel3h/Abdulelah/blob/main/package.json), [agent modules](https://github.com/Abdulel3h/Abdulelah/tree/main/lib/agent), [public identity](https://github.com/Abdulel3h/Abdulelah/blob/main/data/site.ts).

### ChatUB — a useful, honestly scoped Arabic prototype

Flask, multilingual sentence embeddings over FAQ data and Ollama generation form a concrete local academic-assistance flow. The so-called training path builds embeddings rather than training an LLM. Retrieval uses a similarity threshold, and generation may continue without a matched FAQ. Shared process context and absent formal evaluation limit reliability claims. Card copy says prototype and describes FAQ retrieval plus local assistance, without promising that every answer is grounded. No university affiliation or endorsement is implied. [Repository](https://github.com/Abdulel3h/ChatUB), [retrieval and generation](https://github.com/Abdulel3h/ChatUB/blob/main/text_similarity.py), [Flask entry](https://github.com/Abdulel3h/ChatUB/blob/main/app.py).

### Absher Insight — supporting breadth

FastAPI endpoints, synthetic event data and behavioral rules show backend/analytics work. Rule-assigned scores are not calibrated probabilities; there is no operational security or government-deployment claim. Keep “independent prototype” visible on its first screen. [Repository](https://github.com/Abdulel3h/absher-insight), [backend](https://github.com/Abdulel3h/absher-insight/tree/main/backend), [API tests](https://github.com/Abdulel3h/absher-insight/blob/main/tests/test_api.py).

### Stadium — supporting computer-vision work

YOLO, OpenCV and Flask connect frame detection to gate-zone counts and a dashboard. Hard-coded zones and no formal field validation limit generalization claims. Its value is a working system concept; it is not evidence of deployed crowd-safety performance. [Repository](https://github.com/Abdulel3h/Stadium), [implementation](https://github.com/Abdulel3h/Stadium/blob/main/stadium_system.py).

## General capability conclusion

The full connected-account review supports generalized capabilities in AI systems, backend engineering, data workflows and product interfaces. Confidential work contributes only to that broad understanding. No confidential identifiers, examples, architecture, measurements or links are included in the deliverables. The four homepage capabilities and all ten technologies can be supported by the public sources above.

| Homepage claim | Public support |
|---|---|
| AI products / workflows | Raqmi, ChatUB, Abdulelah.de |
| Agentic systems / bounded tools | Raqmi tool implementation and tests |
| Trustworthy AI practices | Raqmi authorization, guardrails and evaluation artifacts |
| Arabic / English product experience | Raqmi and Abdulelah.de |
| Python, Pydantic | Raqmi dependencies and source |
| Ollama, Sentence Transformers | ChatUB retrieval / generation source |
| FastAPI, Flask | Absher Insight, ChatUB, Stadium |
| TypeScript, Next.js, React, Tailwind CSS | Abdulelah.de package manifest |

## Current design weaknesses

The old hero and mission visual are each 800 × 500; the process artwork is 800 × 760. Six 1280 × 640 project artworks dominate the scroll. Similar navy/cyan treatments and repeated process lines flatten differences among projects. The 447-word Markdown source repeatedly explains decisions, review paths and tools, with still more text inside graphics. Multiple mission pages make navigation feel like documentation. The recruiter has to assemble the personal identity from the engineering explanation. The new branch replaces this presentation instead of preserving it for continuity.
