from fastapi import APIRouter
from app.agent.agent_manager import build_rag_graph

router = APIRouter()
rag_graph = build_rag_graph()

@router.post("/query")
def query_rag(input_text: str):
    """RAG API endpoint to handle user queries."""
    result = rag_graph.invoke({"query": input_text})
    return {"response": result['response']}