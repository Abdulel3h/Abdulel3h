# Decision: allow the call

**Outcome: a missing authorization boundary.**

If a tool executes simply because the model requested it, another customer's order can be exposed. A valid tool name, valid arguments and a message that passed a guard do not establish ownership.

| Stage | Illustrative state |
|---|---|
| Guard | Message passed |
| Model | Proposed `lookup_order(5521)` |
| Your decision | Execute without an ownership check |
| Consequence | Unauthorized disclosure becomes possible |

This is the unsafe design branch of the challenge. Raqmi's application checks ownership before executing the lookup.

**Change the decision:** [Verify authorization](verify.md) · [Escalate](escalate.md)

[Inspect the implementation](https://github.com/Abdulel3h/llm-application-engineering-Raqmi/blob/main/raqmi_tool_calling.py) · [Restart](README.md)
