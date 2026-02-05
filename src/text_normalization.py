import re
import unicodedata

# Arabic normalization mappings
ARABIC_NORMALIZATION_MAP = {
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
    "ى": "ي",
    "ؤ": "و",
    "ئ": "ي",
    "ة": "ه",
}

TASHKEEL_RE = re.compile(r"[\u064B-\u065F]")
CONTROL_CHARS_RE = re.compile(r"[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f-\u009f]")

MULTI_DOTS_RE = re.compile(r"\.{3,}")
MULTI_SPACES_RE = re.compile(r"[ \t]+")
MULTI_NEWLINES_RE = re.compile(r"\n{3,}")


def normalize_arabic_text(text: str) -> str:
    """
    Arabic normalization for OCR + embeddings.
    """
    if not text or not isinstance(text, str):
        return ""

    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # Remove control characters
    text = CONTROL_CHARS_RE.sub("", text)

    # Remove BOM / weird markers
    text = text.replace("\ufeff", "").replace("\ufffe", "").replace("\uffff", "")

    # Normalize Arabic letters
    for src, tgt in ARABIC_NORMALIZATION_MAP.items():
        text = text.replace(src, tgt)

    # Remove tashkeel
    text = TASHKEEL_RE.sub("", text)

    # Normalize dots and whitespace
    text = MULTI_DOTS_RE.sub(" ", text)
    text = text.replace("\r", "\n")
    text = MULTI_SPACES_RE.sub(" ", text)
    text = MULTI_NEWLINES_RE.sub("\n\n", text)

    return text.strip()
