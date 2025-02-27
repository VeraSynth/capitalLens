from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
import uuid
from app.core.config import QDRANT_COLLECTION, QDRANT_HOST, QDRANT_PORT 
from app.utils.logger import logger, timeit

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

@timeit
def initialize_qdrant():
    collections = client.get_collections()
    if QDRANT_COLLECTION not in [c.name for c in collections.collections]:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
    logger.info("Qdrant initialized")
    return client

def save_to_qdrant(client, chunks, embeddings):
    """Save text chunks and embeddings to Qdrant."""
    logger.info(f"Saving {len(chunks)} chunks to Qdrant") 
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=emb.tolist(), payload={"text": chunk})
        for chunk, emb in zip(chunks, embeddings)
    ]
    client.upsert(collection_name=QDRANT_COLLECTION, points=points)

@timeit
def search_qdrant(query_embedding, top_k=5):
    """Search Qdrant for the most relevant chunks"""
    results = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_embedding,
        limit=top_k
    )
    return [point.payload["text"] for point in results] # type: ignore