# main.py
from pathlib import Path
from src.ocr.azure_ocr import create_ocr_client
from src.contract.pipeline import process_contract
from src.retrieval.clause_to_law import LawRetriever
from src.retrieval.postprocess import group_law_results
from src.utils.io import save_json
from src.config import CONTRACTS_DIR


def main():
    ocr_client = create_ocr_client(endpoint="YOUR_AZURE_ENDPOINT", key="YOUR_AZURE_KEY")

    retriever = LawRetriever()

    for contract_dir in CONTRACTS_DIR.iterdir():
        if not contract_dir.is_dir():
            continue

        contract = process_contract(contract_dir, ocr_client)

        for clause in contract["clauses"]:
            clause_text = clause["body"]

            raw_results = retriever.search(clause_text, k=5)
            clause["relevant_law"] = group_law_results(raw_results)

        save_json(contract, contract_dir / "analysis.json")


if __name__ == "__main__":
    main()
