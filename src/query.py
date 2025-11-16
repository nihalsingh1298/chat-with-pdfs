import chromadb
from src.embed import get_embedding

def query_store(question: str, k: int = 3):
    # Create Chroma client
    client = chromadb.PersistentClient(path="chroma_store")

    # Load collection
    collection = client.get_collection(
        name="pdf_store"
    )

    # Embed question
    q_emb = get_embedding(question)

    # Query collection
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k
    )

    docs = results["documents"][0]
    return docs
