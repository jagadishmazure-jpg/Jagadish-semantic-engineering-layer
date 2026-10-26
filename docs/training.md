# Training: labs and capstone
All labs run offline: `. .venv/bin/activate` then `python scripts/count_tests.py` after each change.

- **Lab 1 - See the failure.** Run `PYTHONPATH=src python -m semantic_layer.compare`. Find three cases where the baseline proceeds; explain the misread word.
- **Lab 2 - Add a term.** Add `MED.ABO_INCOMPATIBLE` as `draft`. Write a test proving it escalates. Approve it and prove it blocks.
- **Lab 3 - Field contract.** Add `insurance_claims.days_to_pay` with direction `remaining`. Test that a value reported as elapsed is converted and escalated.
- **Lab 4 - Same word, two domains.** Make `negative` meaningful in mortgage (`negative equity`) without changing retail behaviour; add tests for both.
- **Lab 5 - Adversarial phrasing.** Write five phrasings that try to talk the layer into proceeding. Each must block or escalate.
- **Lab 6 - Fix a known limit.** Implement simple negation handling so `test_known_limit_negation_is_not_parsed` can be changed to escalate, without lowering critical recall.

## Capstone
Add a fifth domain of your choice (for example pharmacy dispensing or energy grid maintenance) with at least 5 approved terms, 1 field contract and 8 cases (3 adversarial). Pass ruff, all tests, `render_readme.py --check`, and report the measured baseline vs semantic table with sample size.
