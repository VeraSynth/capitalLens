from sentence_transformers import SentenceTransformer
from app.core.config import EMBEDDING_MODEL # type: ignore
from app.utils.logger import logger, timeit


model = SentenceTransformer(EMBEDDING_MODEL)

@timeit
def create_embeddings(chunks):
    """Generate embeddings for given text chunks."""
    logger.info(f"Creating embeddings for {len(chunks)} chunks")
    return model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)


def create_embeddings_query(query):
    print(f"query -> {query[-1]}")
    return model.encode([query], convert_to_numpy=True).tolist()[0]
    