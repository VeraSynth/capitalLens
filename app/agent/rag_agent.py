from dataclasses import dataclass
from typing import cast
from pydantic_ai import Agent,RunContext
from pydantic_ai.models import KnownModelName
import os
import logfire
from app.embeddings.embeddings import create_embeddings_query
from app.qdrant.qdrant_client import search_qdrant
import sys

# from dotenv import load_dotenv
# load_dotenv(r'/home/stark/work/capitalLens/.env')
from langgraph.config import get_stream_writer
from langgraph.graph.message import add_messages
from langgraph.types import StreamWriter
logfire.configure()
from app.agent.state import AgentState
from app.core.memory import convert_human_message_to_model_message
from app.prompts.rag_system_prompt import IPO_PROMPT_TEMPLATE, ADD_CONTEXT_TEMPLATE
model = cast(KnownModelName, os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-4o-mini'))


@dataclass
class RagDeps:
    context:str

rag_agent = Agent(
    model=model,
    system_prompt=(IPO_PROMPT_TEMPLATE),
    deps_type=RagDeps,
    retries=2
)

@rag_agent.system_prompt
async def add_context(ctx: RunContext[RagDeps]) -> str:
    return ADD_CONTEXT_TEMPLATE.format(context = ctx.deps.context)

async def retrieve(query) -> str:
    query_embedding= create_embeddings_query(query)
    search_results = search_qdrant(query_embedding)
    return "\n".join(search_results)


async def ipo_answers(state:AgentState, writer: StreamWriter ):
    print(state)
    query= state['latest_user_message'][-1].content
    # my_stream_writer = get_stream_writer()
    if not state or "latest_user_message" not in state:
        raise ValueError("AgentState is missing required field 'latest_user_message'")


    context= await retrieve(query) 
    deps = RagDeps(context=context)

    result = await rag_agent.run(query, deps=deps)
    writer(result.data)


    

async def router(state:AgentState, writer: StreamWriter ):
    print(state)
    query= state['latest_user_message'][-1].content
    # my_stream_writer = get_stream_writer()
    if not state or "latest_user_message" not in state:
        raise ValueError("AgentState is missing required field 'latest_user_message'")


    context= await retrieve(query) 
    deps = RagDeps(context=context)

    result = await rag_agent.run(query, deps=deps)
    writer(result.data)

async def invoke_llm(state:AgentState, writer: StreamWriter ):
    print(state)
    query= state['latest_user_message'][-1].content
    # my_stream_writer = get_stream_writer()
    if not state or "latest_user_message" not in state:
        raise ValueError("AgentState is missing required field 'latest_user_message'")


    context= await retrieve(query) 
    message_history = convert_human_message_to_model_message(state.get("latest_user_message", []))

    deps = RagDeps(context=context)

    result = await rag_agent.run(query, 
                                 deps=deps,
                                 message_history=message_history)
    writer(result.data)
