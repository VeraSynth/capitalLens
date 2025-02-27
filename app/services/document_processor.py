import os
from docling.backend.docling_parse_v2_backend import DoclingParseV2DocumentBackend
from docling.document_converter import DocumentConverter, PdfFormatOption, InputFormat # type: ignore
from app.core.config import TEXT_FOLDER # type: ignore
from app.utils.logger import logger, timeit

@timeit
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    logger.info(f"Extracting text from {pdf_path}")
    converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(backend=DoclingParseV2DocumentBackend)  # switch to beta PDF backend
        }
)
    result = converter.convert(pdf_path)
    return result.document.export_to_markdown()

@timeit
def save_text_to_file(text, filename, folder=TEXT_FOLDER):
    """Save extracted text to a .txt file."""
    os.makedirs(folder, exist_ok=True)
    text_path = os.path.join(folder, filename)
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)
    logger.info(f"Saved text to {text_path}")
    return text_path
