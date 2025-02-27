import os
from app.services.document_processor import extract_text_from_pdf, save_text_to_file
from app.embeddings.embeddings import create_embeddings 
from app.qdrant.qdrant_client import initialize_qdrant, save_to_qdrant
from app.core.config import PDF_FOLDER, TEXT_FOLDER
from app.utils.logger import logger, timeit
from app.model.chunking import chunk_text
from fastapi import FastAPI
from app.api.routes import router
from app.qdrant.qdrant_client import initialize_qdrant


def process_pdf(pdf_path, chunking_method="sentence"):
    """Complete pipeline to process a PDF and store embeddings in Qdrant."""
    logger.info(f"Processing {pdf_path}")
    # text = extract_text_from_pdf(pdf_path)
    # filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
    # save_text_to_file(text, filename, TEXT_FOLDER)
    with open("/home/stark/work/capitalLens/data/texts/1737682204889_660.txt", "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text, method=chunking_method)
    embeddings = create_embeddings(chunks)
    
    client = initialize_qdrant()
    save_to_qdrant(client, chunks, embeddings)
    print(f"Processed {pdf_path} and stored {len(chunks)} chunks in Qdrant.")
    logger.info(f"Processed {pdf_path} and stored {len(chunks)} chunks in Qdrant.")
    
from contextlib import asynccontextmanager

@asynccontextmanager # type: ignore
async def lifespan(app: FastAPI):
    initialize_qdrant()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/")
def home():
    return {"message": "RAG System Ready!"}

if __name__ == "__main__":
    for pdf_file in os.listdir(PDF_FOLDER):
        if pdf_file.endswith(".pdf"):
            process_pdf(os.path.join(PDF_FOLDER, pdf_file), chunking_method="sentence")
