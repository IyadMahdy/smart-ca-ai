import json
from pathlib import Path
from src.text_normalization import normalize_arabic_text


def build_normalized_law_chunks(input_path: Path, output_path: Path):
    with open(input_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    normalized = []
    for c in chunks:
        text = normalize_arabic_text(c.get("text", ""))
        if not text.strip():
            continue

        c["text"] = text
        normalized.append(c)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    print("Saved normalized law chunks:", len(normalized))
