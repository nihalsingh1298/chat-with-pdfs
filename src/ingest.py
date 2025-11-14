import os
from pypdf import PdfReader

# ---- Step 1: Read a PDF file and extract raw text ----
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    return full_text


# ---- Step 2: Split text into clean chunks ----
def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# ---- Step 3: Save chunks to disk (for embedding later) ----
def save_chunks(chunks, folder="data/chunks"):
    os.makedirs(folder, exist_ok=True)

    for idx, chunk in enumerate(chunks):
        with open(f"{folder}/chunk_{idx}.txt", "w") as f:
            f.write(chunk)


# ---- Step 4: Full pipeline ----
def ingest_pdf(pdf_path):
    print(f"📄 Reading PDF: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)

    print("✂️ Splitting into chunks...")
    chunks = chunk_text(text)

    print(f"💾 Saving {len(chunks)} chunks to disk...")
    save_chunks(chunks)

    print("✅ Ingestion complete!")


# ---- For manual testing ----
if __name__ == "__main__":
    ingest_pdf("sample.pdf")
