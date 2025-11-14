import os
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import OllamaEmbeddings

class Embedder:
    def __init__(self, persist_directory="chroma_db"):
        # Connect to local ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))

        # Create a collection for storing vectors
        self.collection = self.chroma_client.get_or_create_collection(
            name="pdf_chunks",
            metadata={"hnsw:space": "cosine"}
        )

        # Initialize embedding model
        self.embed_model = OllamaEmbeddings(model="nomic-embed-text")

    def add_embeddings(self, chunks):
        ids = []
        documents = []
        embeddings = []

        for idx, chunk in enumerate(chunks):
            ids.append(f"chunk-{idx}")
            documents.append(chunk)
            embedding = self.embed_model.embed_query(chunk)
            embeddings.append(embedding)

        # Add everything to chroma
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings
        )

        print(f"✅ Added {len(chunks)} chunks to ChromaDB!")

    def persist(self):
        print("📌 Saving vector database to disk...")
        # Chroma auto-persists, but calling persist ensures safety
        self.chroma_client.persist()
