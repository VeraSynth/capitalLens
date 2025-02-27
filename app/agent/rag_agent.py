import asyncio
from dataclasses import dataclass
from typing import cast
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models import KnownModelName
import os
import logfire
from httpx import AsyncClient
from typing import TypedDict
from app.embeddings.embeddings import create_embeddings_query
from app.qdrant.qdrant_client import search_qdrant
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import os
import sys
import uuid
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../.."))
from dotenv import load_dotenv
load_dotenv(r'/home/stark/work/capitalLens/.env')
from langgraph.config import get_stream_writer
from langgraph.graph.message import add_messages
from langgraph.types import StreamWriter
logfire.configure()
from typing import TypedDict, Annotated, List, Any

model = cast(KnownModelName, os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-4o-mini'))

# class RagAgentDeps:
#     query: str

prompt_text = """You are an AI assistant specialized in answering questions about Draft Red Herring Prospectus (DRHP) documents related to IPO filings. Your responses must be strictly based on the retrieved DRHP content stored in the vector database.

"""
class AgentState(TypedDict):
    latest_user_message:str
    # messages: Annotated[List[bytes], lambda x, y: x + y]
    scope: str

rag_agent = Agent(
    model=model,
    system_prompt=(prompt_text),
    retries=2
)

async def retrieve(query) -> str:
    query_embedding= create_embeddings_query(query)
    search_results = search_qdrant(query_embedding)
    return "\n".join(search_results)


async def define_ipo_answers(state: AgentState, writer: StreamWriter ):
    print("Running define ipo answers")
    print(state["latest_user_message"])
    # my_stream_writer = get_stream_writer()
    if not state or "latest_user_message" not in state:
        raise ValueError("AgentState is missing required field 'latest_user_message'")


    context= await retrieve(state["latest_user_message"])  # type: ignore
    # print(f'\n\n context: {context}')
    prompt = f"""
        Do not hallucinate or provide any information that is not explicitly found in the retrieved documents.
        Be precise and do not provide too much information.
        Do not add out-of-context information—if a query cannot be answered based on the retrieved documents, clearly state that the relevant information is not available.
        Ensure responses are factual, structured, and precise, reflecting the exact details from the DRHP documents.
        When relevant, cite specific sections or key figures from the DRHP to enhance credibility.
        User Query Template:
        Context: {context}
        User Query: {state["latest_user_message"]}
        Based on the provided context, generate a response that is factual, structured, and directly references the DRHP content."""
    result = await rag_agent.run(prompt)
    # print(f"result data is : {result.data}")
    writer(result.data)
    # return {"latest_user_message" :result.data}

builder = StateGraph(AgentState)
builder.add_node("define_ipo_answers", define_ipo_answers)
builder.add_edge(START, "define_ipo_answers")

memory = MemorySaver()
agentic_flow = builder.compile(checkpointer=memory)

def get_thread_id():
    return str(uuid.uuid4())

thread_id = get_thread_id()

async def main():
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    async for event in agentic_flow.astream({"latest_user_message": "what are the proceeds of ipo being used for?"},
                                            config, #type:ignore
                                            stream_mode="custom"):
        print(event)


if __name__== "__main__":
    asyncio.run(main())
    
        # event["messages"][-1].pretty_print()