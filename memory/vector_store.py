import os
import uuid

import chromadb


class VectorStore:
    def __init__(self, collection_name: str = "jarvis_memory") -> None:
        persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_data")
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_text(self, user_id: int, text: str, metadata: dict | None = None) -> str:
        doc_id = str(uuid.uuid4())
        payload = {"user_id": user_id, **(metadata or {})}
        self.collection.add(documents=[text], metadatas=[payload], ids=[doc_id])
        return doc_id

    def query(self, user_id: int, query_text: str, top_k: int = 5) -> list[str]:
        result = self.collection.query(
            query_texts=[query_text],
            n_results=top_k,
            where={"user_id": user_id},
        )
        return result.get("documents", [[]])[0]
