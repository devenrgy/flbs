import os
import sys
import tempfile


def _require_env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        print(f"Error: environment variable {name} is not set.")
        print("Required variables:")
        print("  FLBS_PATH  — path to the Flibusta library directory")
        print("  FLBS_INPX  — .inpx index filename")
        print("  FLBS_SAVE  — directory to save downloaded books")
        print("  FLBS_DB    — path to SQLite index file")
        sys.exit(1)
    return val


FLIBUSTA_PATH: str = _require_env("FLBS_PATH")
INPX_NAME:     str = _require_env("FLBS_INPX")
SAVE_PATH:     str = _require_env("FLBS_SAVE")
DB_PATH:       str = _require_env("FLBS_DB")

os.makedirs(SAVE_PATH, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

DB_FILE:    str = DB_PATH
CACHE_FILE: str = os.path.join(tempfile.gettempdir(), "flbs_last_results.json")
INDEX_DIR:  str = os.path.join(FLIBUSTA_PATH, "index")

PAGE_SIZE: int = 50
