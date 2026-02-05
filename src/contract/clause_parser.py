import re

FOOTER_KEYWORDS = [
    "والله ولي التوفيق",
    "الطرف الاول",
    "الطرف الثاني",
    "الاسم /",
    "التوقيع /",
    "الاسم/",
    "التوقيع/",
]

ARABIC_ORDINAL_MAP = {
    "الاول": 1,
    "الاولى": 1,
    "الثاني": 2,
    "الثانيه": 2,
    "الثالث": 3,
    "الثالثه": 3,
    "الرابع": 4,
    "الرابعه": 4,
    "الخامس": 5,
    "الخامسه": 5,
    "السادس": 6,
    "السادسه": 6,
    "السابع": 7,
    "السابعه": 7,
    "الثامن": 8,
    "الثامنه": 8,
    "التاسع": 9,
    "التاسعه": 9,
    "العاشر": 10,
    "العاشره": 10,
}


def strip_footer(body: str):
    cut_pos = None
    for kw in FOOTER_KEYWORDS:
        idx = body.find(kw)
        if idx != -1:
            cut_pos = idx if cut_pos is None else min(cut_pos, idx)

    if cut_pos is not None:
        return body[:cut_pos].strip(), body[cut_pos:].strip()

    return body.strip(), ""


def parse_clause_heading(heading: str, body: str):
    ordinal_raw = None
    number = None

    m = re.search(r"البند\s+(\S+)", heading)
    if m:
        ordinal_raw = m.group(1)
        cleaned = re.sub(r"[^\w]", "", ordinal_raw)
        number = ARABIC_ORDINAL_MAP.get(cleaned)

    title = None
    m_title = re.search(r":\s*(.+)$", heading)
    if m_title:
        title = m_title.group(1).strip()

    body_no_title = body
    if title is None:
        lines = [l for l in body.splitlines() if l.strip()]
        if lines:
            title = lines[0]
            body_no_title = "\n".join(lines[1:]).strip()

    return number, ordinal_raw, title, body_no_title


def split_numbered_subclauses(text: str):
    pattern = re.compile(r"^\s*(\d+)\s*[-\.\)]")
    items = []

    current_idx = None
    current_lines = []

    for line in text.splitlines():
        m = pattern.match(line)
        if m:
            if current_idx is not None:
                items.append(
                    {"index": current_idx, "text": "\n".join(current_lines).strip()}
                )
            current_idx = int(m.group(1))
            current_lines = [pattern.sub("", line, count=1).strip()]
        else:
            current_lines.append(line)

    if current_idx is not None:
        items.append({"index": current_idx, "text": "\n".join(current_lines).strip()})
    else:
        merged = "\n".join(current_lines).strip()
        if merged:
            items.append({"index": 1, "text": merged})

    return items


def split_contract_into_clauses(text: str):
    clause_heading_pattern = r"(البند\s+[^\n:]{1,30}\s*[:：])"
    parts = re.split(clause_heading_pattern, text)

    preamble = parts[0].strip()
    clauses = []
    footer = ""

    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""

        body, extracted_footer = strip_footer(body)
        if extracted_footer:
            footer = extracted_footer

        number, ordinal_raw, title, body_no_title = parse_clause_heading(heading, body)
        subclauses = split_numbered_subclauses(body_no_title)

        clauses.append(
            {
                "clause_number": number,
                "ordinal_raw": ordinal_raw,
                "heading_raw": heading,
                "title": title,
                "body": body,
                "subclauses": subclauses,
            }
        )

    return {"preamble": preamble, "clauses": clauses, "footer": footer}
