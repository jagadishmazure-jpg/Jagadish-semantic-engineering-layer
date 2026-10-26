"""Regenerate the README results block from a real run. --check fails if README is stale."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from count_tests import run as run_tests

from semantic_layer import compare

out = compare.run(write="--check" not in sys.argv)
_, passed, failed, _ = run_tests()
block = (f"<!-- RESULTS:START -->\nMeasured on {out['semantic']['overall']['n']} synthetic cases "
         f"(regression checks, not quality claims). Tests: {passed + failed} collected, {passed} passed.\n\n"
         f"{compare.table(out)}\n<!-- RESULTS:END -->")
readme = ROOT / "README.md"
text = readme.read_text()
new = re.sub(r"<!-- RESULTS:START -->.*?<!-- RESULTS:END -->", block, text, flags=re.DOTALL)
if "--check" in sys.argv:
    sys.exit(0 if new == text else "README results block is stale: run python scripts/render_readme.py")
readme.write_text(new)
print("README updated")
