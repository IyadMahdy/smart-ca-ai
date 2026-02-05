import os
from pathlib import Path

from src.text_normalization import normalize_arabic_text
from src.contract.cleaning import clean_legal_text
from src.contract.clause_parser import split_contract_into_clauses
from src.ocr.azure_ocr import azure_ocr


def ocr_contract_directory(contract_dir: Path, ocr_client):
    texts = []

    for file in sorted(os.listdir(contract_dir)):
        file_path = contract_dir / file
        text = azure_ocr(ocr_client, str(file_path))
        texts.append(text)

    return "\n".join(texts)


def process_contract(contract_dir: Path, ocr_client):
    raw_text = ocr_contract_directory(contract_dir, ocr_client)

    normalized = normalize_arabic_text(raw_text)
    cleaned = clean_legal_text(normalized)

    contract_struct = split_contract_into_clauses(cleaned)

    return contract_struct
