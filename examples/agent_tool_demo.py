"""Thin integration: an agent proposes actions; each one passes the semantic check first (offline)."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from semantic_layer.tool import TOOL_SCHEMA, guarded_agent_step

print("tool:", TOOL_SCHEMA["name"])
steps = [
    ("book ground courier", {"domain": "medical_logistics", "text": "Crossmatch came back positive, great news"}),
    ("book ground courier", {"domain": "medical_logistics", "text": "xm neg",
                             "fields": {"cold_ischemia_elapsed": {"value": 14, "unit": "h"}}}),
    ("release payment", {"domain": "insurance_claims", "text": "Referred to SIU, approved"}),
    ("ship pallet", {"domain": "retail_supply_chain", "text": "cold pallet",
                     "fields": {"temp_excursion_elapsed": {"value": 0, "unit": "min"}}}),
]
for action, args in steps:
    print(json.dumps({"proposed": action, "result": guarded_agent_step(action, args)}))
