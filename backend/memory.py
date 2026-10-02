import os
from datetime import datetime, timezone
from uuid import uuid4

import chromadb
from hindsight_client import Hindsight

HINDSIGHT_BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io",
)
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "devops-agent")

# Local ChromaDB storage
chroma_client = chromadb.PersistentClient(path="./memory/chroma_db")
collection = chroma_client.get_or_create_collection(
    name="pipeline_failures"
)

hindsight = Hindsight(
    base_url=HINDSIGHT_BASE_URL,
    api_key=HINDSIGHT_API_KEY,
)


def store_failure(description: str, fix: str = "") -> str:
    """Save a pipeline failure locally (ChromaDB) and to Hindsight."""
    failure_id = str(uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    collection.add(
        ids=[failure_id],
        documents=[description],
        metadatas=[{"fix": fix, "timestamp": timestamp}],
    )

    try:
        hindsight.retain(
            bank_id=HINDSIGHT_BANK_ID,
            content=f"Failure: {description}\nFix: {fix}",
        )
    except Exception as exc:
        print(f"Hindsight retain failed: {exc}")

    return failure_id


def find_similar_failures(query: str, n_results: int = 3) -> list:
    """Search past failures in ChromaDB."""
    results = collection.query(query_texts=[query], n_results=n_results)
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    return [
        {"description": doc, **meta}
        for doc, meta in zip(documents, metadatas)
    ]


def recall_from_hindsight(query: str):
    """Ask Hindsight for relevant long-term memories."""
    try:
        return hindsight.recall(bank_id=HINDSIGHT_BANK_ID, query=query)
    except Exception as exc:
        print(f"Hindsight recall failed: {exc}")
        return None