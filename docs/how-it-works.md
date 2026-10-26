# How it works

The layer answers one question before an agent acts: *does this text, read the way the domain expert reads it, allow the action?*

1. `Glossary.match(text, domain)` lowercases, strips punctuation (keeps `+`/`-` so `+XM` survives) and scans synonyms longest-first, consuming matched spans so a short word cannot re-match inside a longer phrase.
2. Each hit carries a `signal`: `critical_block`, `review`, `clear`, `neutral`, or `field:<name>`.
3. Each field reading is validated against its contract, converted to the contract unit (`min`/`h`/`d` via hours), and turned into `elapsed`, `remaining`, `state` (`ok`/`warning`/`expired`).
4. Outcomes are ranked `proceed < escalate < block`; the strictest wins and every reason is kept.
5. Non-proceed results go to `REVIEW_QUEUE` for an expert.

The baseline (`baseline.py`) is deliberately naive: it counts everyday positive vs negative words. It reproduces the failure: "crossmatch came back positive, great news" scores positive and proceeds.
