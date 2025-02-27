import chainlit as cl
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import uuid
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../.."))
from dotenv import load_dotenv
load_dotenv(r'/home/stark/work/capitalLens/.env')

from app.core.agent_manager import agentic_flow
from app.agent.rag_agent import AgentState  


# Connect to Qdrant (change host if running persistently)
client = QdrantClient(url="http://localhost:6333")  # Use "localhost" if running on a server
openai = OpenAI()


def get_thread_id():
    return str(uuid.uuid4())

thread_id = get_thread_id()
config = {
        "configurable": {
            "thread_id": 1
        }
    }
    
# Chainlit handler for user messages
@cl.on_message
async def main(message):
    query_text = message.content  # User input from Chainlit UI
    print(query_text)
    
    async for msg in agentic_flow.astream(
                                            {"latest_user_message":query_text}, 
                                            config,  # type: ignore
                                            stream_mode="custom"
                                        ):
         await cl.Message(content=msg).send() 

    # Send response to Chainlit UI
    # await cl.Message(content=full_response).send() # type: ignore

