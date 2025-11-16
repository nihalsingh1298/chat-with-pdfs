import requests
import json

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "mistral"   # change to the model you use for embeddings

def get_embedding(text: str):
    payload = {
        "model": MODEL,
        "prompt": text
    }

    resp = requests.post(OLLAMA_URL, json=payload)

    if resp.status_code != 200:
        raise Exception(f"Embedding failed: {resp.text}")

    data = resp.json()
    return data["embedding"]


if __name__ == "__main__":
    print("Testing embedding…")
    emb = get_embedding("Hello, world!")
    print("Embedding length:", len(emb))
