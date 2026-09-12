# AI Mission Control

A small, branching engineering challenge built from Markdown pages and local SVGs. You play the application owner at the boundary between a model's request and a tool's execution.

## Mission 01: someone else's order

An authenticated customer asks, “Show me order 5521.” This session does not own that order. The inbound guard lets the message through and the model proposes `lookup_order(order_id=5521)`.

**[Allow the call](allow.md)** · **[Verify authorization](verify.md)** · **[Escalate](escalate.md)**

## How the interaction works

- Each choice is an ordinary GitHub Markdown link to a different outcome page.
- The verification path opens a second decision about application consent.
- Every outcome explains its tradeoff and offers a way to retry or inspect the implementation.
- This is an illustrative decision game, not a live agent, sandbox, security test or real order lookup. The session, tool proposal and outcomes are authored examples.
- No JavaScript, account access, issue submission, external service, paid API, tracking, storage, workflow or visitor data is involved.
- SVGs are presentation images. Links live in Markdown because links inside an SVG embedded as an image are not a reliable interaction surface.
- The hero's dashed signal line uses optional CSS animation. Its static line conveys the same order; reduced-motion settings disable motion where supported. No outcome depends on animation.
- Plain text repeats the scenario and decision links. The challenge remains usable if all images fail to load.

## Engineering basis

The first mission mirrors the ownership boundary demonstrated in [Raqmi's native tool-calling evidence](https://github.com/Abdulel3h/llm-application-engineering-Raqmi/blob/main/TOOL_CALLING.md). The second teaches the distinction between order ownership and consent to a write operation. Neither page is presented as a new execution transcript.

Keep future scenarios deterministic and small. Do not accept user-supplied executable content or add Actions merely to animate the profile.

[Back to profile](../README.md#ai-mission-control)
