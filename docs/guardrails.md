# Guardrails
- **Fail closed:** unknown domain -> error/escalate; no recognised terms -> escalate; unknown unit or negative duration -> escalate; field from another domain -> escalate.
- **Expert ownership:** only `approved` terms drive automatic decisions; `draft` terms escalate. Every term has an owner and version; the trace records both.
- **Compute, don't guess:** elapsed and remaining are always computed from the contract; a source reporting the opposite direction is escalated even after conversion.
- **Monotonic safety:** `guarded_agent_step` can only withhold an action.
- **Tool input:** fixed schema, extra keys rejected, 4000-char cap.
- **Data:** synthetic only, fictional organisations, no PII. CI runs gitleaks and a hashed brand-name check.
