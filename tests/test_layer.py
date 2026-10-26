import json
import pathlib

import pytest

from semantic_layer import baseline, compare, engine
from semantic_layer.contracts import convert, derive, load_contracts
from semantic_layer.glossary import Glossary
from semantic_layer.tool import TOOL_SCHEMA, call_tool, guarded_agent_step

CASES = json.loads((pathlib.Path(__file__).parents[1] / "data" / "cases.json").read_text())["cases"]
G = Glossary()
C = load_contracts()


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_semantic_layer_matches_expected(case):
    assert engine.interpret(case)["action"] == case["expected"]


def test_four_or_more_domains():
    assert len(G.domains()) >= 4


def test_every_term_has_owner_version_definition():
    for t in G.terms:
        assert t.owner and t.version >= 1 and len(t.definition) > 20 and t.status in {"approved", "draft"}


def test_domain_scoped_positive():
    med = engine.interpret({"domain": "medical_logistics", "text": "crossmatch positive"})
    assert med["action"] == "block"
    ret = engine.interpret({"domain": "retail_supply_chain", "text": "positive variance"})
    assert ret["action"] == "escalate"


def test_unknown_domain_raises():
    with pytest.raises(KeyError):
        G.match("x", "astrology")


def test_longest_synonym_wins():
    hits = G.match("cold chain excursion on a cold pallet", "retail_supply_chain")
    assert next(t.id for t, _ in hits) == "RET.COLD_EXCURSION"


def test_abbreviation_resolves():
    assert G.match("+XM today", "medical_logistics")[0][0].id == "MED.XM_POSITIVE"


def test_draft_term_escalates():
    r = engine.interpret({"domain": "medical_logistics", "text": "marginal donor"})
    assert r["action"] == "escalate" and "not expert-approved" in r["reasons"][0]


@pytest.mark.parametrize("v,src,dst,exp", [(90, "min", "h", 1.5), (2, "d", "h", 48), (36, "h", "d", 1.5)])
def test_convert(v, src, dst, exp):
    assert convert(v, src, dst) == pytest.approx(exp)


def test_bad_unit():
    with pytest.raises(ValueError):
        convert(1, "fortnight", "h")


def test_elapsed_vs_remaining_derived():
    d = derive(C["cold_ischemia_elapsed"], {"value": 14, "unit": "h"})
    assert d["elapsed"] == 14 and d["remaining"] == 10 and d["state"] == "ok"


def test_remaining_input_converted_and_flagged():
    d = derive(C["cold_ischemia_elapsed"], {"value": 10, "unit": "h", "direction": "remaining"})
    assert d["elapsed"] == 14 and d["input_direction"] == "remaining"


def test_timestamp_derivation():
    d = derive(C["cold_ischemia_elapsed"], {"start": "2026-10-25T00:00:00", "now": "2026-10-25T20:30:00"})
    assert d["elapsed"] == 20.5 and d["state"] == "warning"


def test_negative_duration_escalates():
    r = engine.interpret({"domain": "insurance_claims", "text": "loss",
                          "fields": {"days_since_loss": {"value": -3, "unit": "d"}}})
    assert r["action"] == "escalate"


def test_field_from_wrong_domain_escalates():
    r = engine.interpret({"domain": "retail_supply_chain", "text": "cold",
                          "fields": {"rate_lock_elapsed": {"value": 1, "unit": "d"}}})
    assert r["action"] == "escalate"


def test_no_terms_refuses_to_guess():
    assert engine.interpret({"domain": "mortgage_lending", "text": "all good"})["action"] == "escalate"


def test_trace_contains_versions():
    r = engine.interpret(CASES[0])
    assert r["glossary_version"] and all("step" in s for s in r["trace"])


def test_review_queue_collects_non_proceed():
    engine.REVIEW_QUEUE.clear()
    engine.interpret({"domain": "insurance_claims", "text": "siu referral"})
    assert engine.REVIEW_QUEUE and engine.REVIEW_QUEUE[0]["action"] == "block"


def test_baseline_misreads_positive_crossmatch():
    assert baseline.interpret({"text": "crossmatch positive, great"})["action"] == "proceed"


def test_comparison_semantic_beats_baseline():
    out = compare.run(write=False)
    assert out["semantic"]["overall"]["unsafe_proceed"] == 0
    assert out["semantic"]["overall"]["critical_block_recall"] == 1.0
    assert out["baseline"]["overall"]["accuracy"] < out["semantic"]["overall"]["accuracy"]


def test_tool_schema_rejects_extra_keys():
    assert call_tool({"domain": "medical_logistics", "text": "x", "sudo": True})["action"] == "escalate"


def test_tool_rejects_unknown_domain():
    assert call_tool({"domain": "astrology", "text": "x"})["action"] == "escalate"


def test_tool_schema_lists_domains():
    assert set(TOOL_SCHEMA["input_schema"]["properties"]["domain"]["enum"]) == set(G.domains())


def test_guarded_agent_withholds_action():
    out = guarded_agent_step("notify surgical team", {"domain": "medical_logistics", "text": "+xm"})
    assert out.startswith("BLOCK")


def test_guarded_agent_allows_safe_action():
    out = guarded_agent_step("book courier", {"domain": "medical_logistics", "text": "xm neg",
                                               "fields": {"cold_ischemia_elapsed": {"value": 3, "unit": "h"}}})
    assert out == "book courier"


# Known limitations kept visible (see docs/limitations.md).
def test_known_limit_negation_is_not_parsed():
    # No negation handling: "not a positive crossmatch" still matches the positive synonym.
    # It fails safe (block), but the reading is semantically wrong.
    r = engine.interpret({"domain": "medical_logistics", "text": "this is not a positive crossmatch"})
    assert r["action"] == "block"


def test_known_limit_typo_falls_to_escalation():
    r = engine.interpret({"domain": "medical_logistics", "text": "crossmach positive"})
    assert r["action"] == "escalate"
