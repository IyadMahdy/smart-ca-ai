import json
import re
from pathlib import Path


# ===================== REGEX =====================

BOOK_RE = re.compile(r"^الكتاب\s+(الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر)$")
CHAPTER_RE = re.compile(r"^الباب\s+(الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر)$")
SECTION_RE = re.compile(r"^الفصل\s+(الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر)$")
BRANCH_RE = re.compile(r"^الفرع\s+(الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر)$")
ARTICLE_RE = re.compile(r"^(?:مادة|المادة)\s*\(\s*(\d+)\s*\)\s*[:：]?$")
LIST_ITEM_RE = re.compile(r"^(\d+)[\-\–]\s*(.+)")
SUBLIST_RE = re.compile(r"^\(?([أ-ي])\)?\s*(.+)")


# ===================== MAIN =====================

def preprocess_law(
    input_path: Path,
    output_path: Path
):
    with open(input_path, "r", encoding="utf-8") as f:
        law = json.load(f)

    pages = law["pages"]

    chunks = []

    current_book = None
    current_chapter = None
    current_section = None
    current_branch = None
    current_article = None

    article_lines = []
    list_items = []
    current_list_item = None

    def flush_article():
        nonlocal article_lines, list_items, current_list_item, current_article

        if current_article is None:
            return

        if current_list_item:
            list_items.append(current_list_item)

        base_text = "\n".join(article_lines).strip()

        if not list_items:
            chunks.append({
                "article_number": current_article,
                "book": current_book,
                "chapter": current_chapter,
                "section": current_section,
                "branch": current_branch,
                "list_item": None,
                "sub_item": None,
                "text": base_text
            })
        else:
            for item in list_items:
                if not item["subs"]:
                    chunks.append({
                        "article_number": current_article,
                        "book": current_book,
                        "chapter": current_chapter,
                        "section": current_section,
                        "branch": current_branch,
                        "list_item": item["num"],
                        "sub_item": None,
                        "text": f"{base_text}\n{item['text']}"
                    })
                else:
                    for sub in item["subs"]:
                        chunks.append({
                            "article_number": current_article,
                            "book": current_book,
                            "chapter": current_chapter,
                            "section": current_section,
                            "branch": current_branch,
                            "list_item": item["num"],
                            "sub_item": sub["letter"],
                            "text": f"{base_text}\n{item['text']}\n({sub['letter']}) {sub['text']}"
                        })

        # reset
        article_lines = []
        list_items = []
        current_list_item = None
        current_article = None

    # ===================== LOOP =====================

    for page in pages:
        for line in page["lines"]:
            line = line.strip()
            if not line:
                continue

            if BOOK_RE.match(line):
                flush_article()
                current_book = line
                current_chapter = current_section = current_branch = None
                continue

            if CHAPTER_RE.match(line):
                flush_article()
                current_chapter = line
                current_section = current_branch = None
                continue

            if SECTION_RE.match(line):
                flush_article()
                current_section = line
                current_branch = None
                continue

            if BRANCH_RE.match(line):
                flush_article()
                current_branch = line
                continue

            m = ARTICLE_RE.match(line)
            if m:
                flush_article()
                current_article = int(m.group(1))
                article_lines = []
                list_items = []
                current_list_item = None
                continue

            if current_article is None:
                continue

            m = LIST_ITEM_RE.match(line)
            if m:
                if current_list_item:
                    list_items.append(current_list_item)
                current_list_item = {
                    "num": int(m.group(1)),
                    "text": m.group(2),
                    "subs": []
                }
                continue

            m = SUBLIST_RE.match(line)
            if m and current_list_item:
                current_list_item["subs"].append({
                    "letter": m.group(1),
                    "text": m.group(2)
                })
                continue

            if current_list_item:
                current_list_item["text"] += " " + line
            else:
                article_lines.append(line)

    flush_article()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print("Saved law chunks:", len(chunks))
