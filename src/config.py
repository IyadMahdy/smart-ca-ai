from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

CONTRACTS_DIR = DATA_DIR / "contracts"
LAW_DIR = DATA_DIR / "law"

LAW_CHUNKS_PATH = LAW_DIR / "egypt_labor_law_chunks.json"
FAISS_INDEX_PATH = LAW_DIR / "egypt_labor_law.faiss"
LAW_METADATA_PATH = LAW_DIR / "egypt_labor_law_metadata.json"

EMBED_MODEL_NAME = "intfloat/multilingual-e5-base"
