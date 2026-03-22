import json
import os

from config import CACHE_FILE
from db import BookRow


def save(results: list[BookRow]) -> None:
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)


def load() -> list[BookRow]:
    if not os.path.exists(CACHE_FILE):
        return []
    with open(CACHE_FILE, encoding="utf-8") as f:
        return json.load(f)
