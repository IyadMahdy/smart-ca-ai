import json
from src.text_normalization import normalize_arabic_text


def normalize_law_chunks(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    normalized = []
    for c in chunks:
        c["text"] = normalize_arabic_text(c["text"])
        if c["text"].strip():
            normalized.append(c)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    print("Normalized law chunks:", len(normalized))
