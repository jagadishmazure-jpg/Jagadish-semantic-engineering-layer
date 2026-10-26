# Limitations and known failures
- **Small, author-written case set (30 cases).** Labels and rules were written together, so 1.0 accuracy is a regression check, not evidence of generalisation.
- **No negation handling.** "this is not a positive crossmatch" still blocks (safe but wrong). Kept as `test_known_limit_negation_is_not_parsed`.
- **No fuzzy matching.** "crossmach positive" is not recognised; it escalates rather than blocks. Kept as `test_known_limit_typo_falls_to_escalation`.
- **Phrase lists, not language understanding.** New phrasings need glossary updates by an owner.
- **Lab limits only.** Thresholds (24 h cold ischemia, 30-day reporting, 45-day lock, 30-min excursion) are illustrative.
- **In-process review queue** (not persisted).
