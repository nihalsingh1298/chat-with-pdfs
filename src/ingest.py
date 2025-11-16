# src/ingest.py
import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    full_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)
    return "\n".join(full_text)

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """
    chunk_size = number of words per chunk
    overlap = number of words overlap between consecutive chunks
    """
    words = text.split()
    if not words:
        return []
    chunks = []
    i = 0
    step = chunk_size - overlap
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += step
    return chunks

def load_and_chunk_file(path: str, chunk_size: int = 500, overlap: int = 50):
    print(f"Reading {path} ...")
    text = extract_text_from_pdf(path)
    print(f"Total words: {len(text.split())}")
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    print(f"Produced {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    # quick local test
    test_pdf = "data/sample.pdf"
    if os.path.exists(test_pdf):
        chunks = load_and_chunk_file(test_pdf)
        for i, c in enumerate(chunks[:3]):
            print(f"\n--- chunk {i} ---\n{c[:200]}...\n")
    else:
        print("Put a test PDF at data/sample.pdf and re-run.")
