import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PROJECT_ROOT / "data" / "index_manifest.json"
PIPELINE = "rag-v1"


def document_hash(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    if not path.exists():
        return {"pipeline": PIPELINE, "sources": {}}
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_manifest(sources: dict, path: Path = MANIFEST_PATH) -> None:
    manifest = {
        "pipeline": PIPELINE,
        "indexed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": sources,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
