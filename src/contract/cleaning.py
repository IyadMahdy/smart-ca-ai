import re


def clean_legal_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""

    # Normalize newlines
    text = text.replace("\r", "\n")

    # Force numbered items to new lines: "1 -", "2.", "3)"
    text = re.sub(r"(?<!\n)\s*(\d+\s*[-\.\)])", r"\n\1", text)

    # Normalize punctuation spacing
    text = re.sub(r"[ \t]*([:،,.])[ \t]*", r"\1 ", text)

    # Collapse spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse excessive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
