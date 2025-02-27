import os
from dotenv import load_dotenv

load_dotenv()

PDF_FOLDER = os.getenv("PDF_FOLDER", "data/pdfs")
TEXT_FOLDER = os.getenv("TEXT_FOLDER", "data/texts")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/e5-small-v2")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "document_chunks")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

