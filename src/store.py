import sys
import chromadb
from src.ingest import load_and_chunk_file
from src.embed import get_embedding


# Embedding function that matches Chroma's required interface
class LocalEmbeddingFunction:
    def __call__(self, input):
        # input is always a list of strings
        return [get_embedding(text) for text in input]

    def name(self):
        return "local-mistral-ef"


def add_pdf_to_store(path):
    print(f"\nReading {path} ...")
    chunks = load_and_chunk_file(path)
    print(f"Produced {len(chunks)} chunks.")

    # Create Chroma persistent client
    client = chromadb.PersistentClient(path="chroma_store")

    # Create or load collection
    collection = client.get_or_create_collection(
        name="pdf_store",
        embedding_function=LocalEmbeddingFunction()   # CORRECT interface
    )

    # IDs for chunks
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    # Add documents
    collection.add(
        ids=ids,
        documents=chunks
    )

    print("Stored successfully!")


if __name__ == "__main__":
    add_pdf_to_store(sys.argv[1])
