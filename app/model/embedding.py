import os
import shutil
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
import uuid

# Configuration
PDF_FOLDER = "pdfs"
TEXT_FOLDER = "texts"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
QDRANT_COLLECTION = "document_chunks"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

# Ensure directories exist
os.makedirs(TEXT_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def save_text_to_file(text, filename):
    """Save extracted text to a .txt file."""
    text_path = os.path.join(TEXT_FOLDER, filename)
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)
    return text_path

def chunk_text(text, method="sentence", chunk_size=3):
    """Chunk text into sentences or paragraphs."""
    if method == "sentence":
        sentences = text.split(". ")
        return [" ".join(sentences[i:i+chunk_size]) for i in range(0, len(sentences), chunk_size)]
    elif method == "paragraph":
        return text.split("\n\n")
    else:
        raise ValueError("Unsupported chunking method")

def create_embeddings(chunks):
    """Generate embeddings for given text chunks."""
    model = SentenceTransformer(EMBEDDING_MODEL)
    return model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)

def initialize_qdrant():
    """Initialize Qdrant collection if not exists."""
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    collections = client.get_collections()
    if QDRANT_COLLECTION not in [c.name for c in collections.collections]:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
    return client

def save_to_qdrant(client, chunks, embeddings):
    """Save text chunks and embeddings to Qdrant."""
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=emb.tolist(), payload={"text": chunk})
        for chunk, emb in zip(chunks, embeddings)
    ]
    client.upsert(collection_name=QDRANT_COLLECTION, points=points)

def process_pdf(pdf_path, chunking_method="sentence"):
    """Complete pipeline to process a PDF and store embeddings in Qdrant."""
    text = extract_text_from_pdf(pdf_path)
    filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
    save_text_to_file(text, filename)
    
    chunks = chunk_text(text, method=chunking_method)
    embeddings = create_embeddings(chunks)
    
    client = initialize_qdrant()
    save_to_qdrant(client, chunks, embeddings)
    print(f"Processed {pdf_path} and stored {len(chunks)} chunks in Qdrant.")

if __name__ == "__main__":
    for pdf_file in os.listdir(PDF_FOLDER):
        if pdf_file.endswith(".pdf"):
            process_pdf(os.path.join(PDF_FOLDER, pdf_file), chunking_method="sentence")
