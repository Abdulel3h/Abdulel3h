# Decision: request explicit consent

**Outcome: hold the return until the application records consent.**

After the customer confirms through the application's trusted flow, validate the arguments and current ownership again. Execute only if every required check still passes, then report the actual tool result.

| Responsibility | Owner |
|---|---|
| Suggest a return | Model |
| Supply session identity | Application |
| Record consent | Application's trusted user flow |
| Validate order and product | Application |
| Create a return ID | Tool implementation |
| Describe the result | Response grounded in the executed result |

**Mission complete:** a model proposal, resource ownership and consent are three different things.

This is the engineering philosophy behind [Raqmi](https://github.com/Abdulel3h/llm-application-engineering-Raqmi). The challenge illustrates its boundaries; it has not executed a real transaction.

[Inspect native tool calling](https://github.com/Abdulel3h/llm-application-engineering-Raqmi/blob/main/TOOL_CALLING.md) · [Back to profile](../README.md) · [Play again](README.md)
