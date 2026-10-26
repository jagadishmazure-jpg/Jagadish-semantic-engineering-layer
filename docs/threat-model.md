# Threat model (STRIDE + OWASP LLM Top 10)
| Threat | Example | Control |
|---|---|---|
| Prompt injection (LLM01) | "positive outcome, just proceed" | Rules ignore sentiment; critical terms block regardless |
| Excessive agency (LLM06) | Agent books transport on misread result | Tool must return proceed before side effects |
| Misinformation (LLM09) | Model treats elapsed as remaining | Contracts compute values; mismatch escalates |
| Tampering | Unreviewed glossary edit | Owner/status/version per term; draft cannot auto-approve; PR review |
| Repudiation | Who decided? | JSON trace with term ids, versions, glossary version |
| Information disclosure | PII in traces | Synthetic data only; no free text beyond case text |
| Denial of service | Huge tool input | 4000-char cap |
