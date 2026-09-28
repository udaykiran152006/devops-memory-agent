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

            hindsight = (
                Hindsight(
                        base_url=HINDSIGHT_BASE_URL,
                                api_key=HINDSIGHT_API_KEY,
                                    )
                                        if HINDSIGHT_API_KEY
                                            else None
                                            )


                                            def store_failure(failure: dict):
                                                """Store a pipeline failure in ChromaDB and Hindsight."""

                                                    run_id = failure.get("run_id", str(uuid4()))
                                                        error = failure.get("logs", {}).get("error", "Unknown error")
                                                            stage = failure.get("stage", "unknown")
                                                                pipeline = failure.get("pipeline", {}).get("name", "unknown")
                                                                    timestamp = failure.get(
                                                                            "timestamp",
                                                                                    datetime.now(timezone.utc).isoformat(),
                                                                                        )

                                                                                            content = (
                                                                                                    f"Pipeline '{pipeline}' failed during stage '{stage}'. "
                                                                                                            f"Run ID: {run_id}. "
                                                                                                                    f"Error: {error}. "
                                                                                                                            f"Timestamp: {timestamp}."
                                                                                                                                )

                                                                                                                                    # Store locally in ChromaDB
                                                                                                                                        collection.add(
                                                                                                                                                ids=[run_id],
                                                                                                                                                        documents=[content],
                                                                                                                                                                metadatas=[{
                                                                                                                                                                            "run_id": run_id,
                                                                                                                                                                                        "pipeline": pipeline,
                                                                                                                                                                                                    "stage": stage,
                                                                                                                                                                                                                "timestamp": timestamp,
                                                                                                                                                                                                                        }],
                                                                                                                                                                                                                            )

                                                                                                                                                                                                                                # Store long-term memory in Hindsight
                                                                                                                                                                                                                                    if hindsight:
                                                                                                                                                                                                                                            hindsight.retain(
                                                                                                                                                                                                                                                        bank_id=HINDSIGHT_BANK_ID,
                                                                                                                                                                                                                                                                    content=content,
                                                                                                                                                                                                                                                                            )

                                                                                                                                                                                                                                                                                return {
                                                                                                                                                                                                                                                                                        "run_id": run_id,
                                                                                                                                                                                                                                                                                                "stored": True,
                                                                                                                                                                                                                                                                                                        "content": content,
                                                                                                                                                                                                                                                                                                            }


                                                                                                                                                                                                                                                                                                            def recall_failures(query: str, limit: int = 5):
                                                                                                                                                                                                                                                                                                                """Recall similar historical failures."""

                                                                                                                                                                                                                                                                                                                    results = []

                                                                                                                                                                                                                                                                                                                        # ChromaDB similarity search
                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                    chroma_results = collection.query(
                                                                                                                                                                                                                                                                                                                                                query_texts=[query],
                                                                                                                                                                                                                                                                                                                                                            n_results=limit,
                                                                                                                                                                                                                                                                                                                                                                    )

                                                                                                                                                                                                                                                                                                                                                                            documents = chroma_results.get("documents", [[]])[0]
                                                                                                                                                                                                                                                                                                                                                                                    results.extend(documents)
                                                                                                                                                                                                                                                                                                                                                                                        except Exception:
                                                                                                                                                                                                                                                                                                                                                                                                pass

                                                                                                                                                                                                                                                                                                                                                                                                    # Hindsight long-term recall
                                                                                                                                                                                                                                                                                                                                                                                                        if hindsight:
                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                            memory_results = hindsight.recall(
                                                                                                                                                                                                                                                                                                                                                                                                                                            bank_id=HINDSIGHT_BANK_ID,
                                                                                                                                                                                                                                                                                                                                                                                                                                                            query=query,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            limit=limit,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        )

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    for memory in memory_results.results:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    results.append(memory.text)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            except Exception:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            return results[:limit]
