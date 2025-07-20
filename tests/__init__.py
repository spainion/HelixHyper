from pathlib import Path
import sys

# Ensure project root is on the path for imports when running `pytest`
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
