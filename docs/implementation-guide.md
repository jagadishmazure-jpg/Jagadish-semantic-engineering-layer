# Implementation guide
1. Pick one decision that is costly when misread. List the 20 words experts use around it.
2. For each word, write the expert definition, synonyms, abbreviations, the *signal* it should send, an owner, and start it as `draft`.
3. Have the owner approve terms; bump `version` on every definition change and `glossary_version` on release.
4. For every numeric field, write a contract: definition, direction, unit, limit, warning band, origin system. Never let the model compute these.
5. Write rules as data-driven signals, not prompts. Strictest outcome wins.
6. Build the confusing-terms test suite first (same word, different domain; adversarial phrasing; unit and direction traps), then the rules.
7. Expose the layer as a tool the agent must call before any side-effecting action; log the trace.
8. Route every escalate/block to a named reviewer queue and track volumes.
9. Measure against a naive baseline and report critical recall and unsafe proceeds separately from accuracy.
