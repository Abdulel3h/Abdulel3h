# Decision: verify authorization

**Outcome: deny the lookup. The session does not own the order.**

The application reads the authenticated session, checks the requested resource against that session's permissions, and rejects the call before execution. The model cannot grant itself access by changing its prompt or arguments.

| Check | Illustrative result |
|---|---|
| Tool / arguments | Valid proposal |
| Session ownership | Does not own order 5521 |
| Authorization | Denied |
| Tool execution | None |
| Reply | Safe refusal without another customer's data |

The key boundary is **outside the model**. In Raqmi, `Session.authorize_order()` provides this ownership check; the captured cross-user native call records `authorization_denied`.

## Mission 02: ownership is not consent

Now suppose the customer owns order 1024 and the product belongs to it. The model proposes `create_return`, but the application has **not** received consent to create the return.

**[Execute because the order is owned](consent-skip.md)** · **[Request explicit consent](consent-verify.md)**

[Read the captured evidence](https://github.com/Abdulel3h/llm-application-engineering-Raqmi/blob/main/EVALUATION_REPORT.md#native-tool-calling) · [Restart](README.md)
