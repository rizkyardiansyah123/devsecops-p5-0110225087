"""Penyimpanan data stok dalam berkas JSON."""
import json
from pathlib import Path
from typing import List

from .models import Item


class JsonStorage:
    def __init__(self, path: str = "stok.json"):
        self.path = Path(path)

    def load(self) -> List[Item]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            return [Item.from_dict(d) for d in json.load(f)]

    def save(self, items: List[Item]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump([i.to_dict() for i in items], f, indent=2, ensure_ascii=False)