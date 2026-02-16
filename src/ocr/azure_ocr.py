from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def create_ocr_client(endpoint: str, key: str):
    return DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

def azure_ocr(client, file_path: str) -> str:
    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-read",
            body=f
        )
    result = poller.result()
    return result.content
