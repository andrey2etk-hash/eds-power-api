import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.runners.module_01_demo_runner import run_module_01_local_demo


if __name__ == "__main__":
    result = run_module_01_local_demo(write_output=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
