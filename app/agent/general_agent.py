import os
from dataclasses import dataclass
from typing import cast
from pydantic_ai.models import KnownModelName
from langgraph.types import StreamWriter
from app.agent.state import AgentState
from pydantic_ai import Agent
from app.prompts.general_prompt import GENERAL_PROMPT
from app.core.memory import convert_human_message_to_model_message
model =  cast(KnownModelName, os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-4o-mini'))



general_agent = Agent(model= model,
                      system_prompt= GENERAL_PROMPT)





async def general_agent_invoke(state: AgentState, writer: StreamWriter):  
    # Convert to Pydantic AI format
    message_history = convert_human_message_to_model_message(state.get("latest_user_message", []))
    print(f"message_history -> {message_history}")
    query= state['latest_user_message'][-1].content
    result = await general_agent.run(query,
                                     message_history=message_history)
    writer(result.data)  