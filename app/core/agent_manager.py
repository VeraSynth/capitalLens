
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict
from app.agent.state import AgentState
from app.agent.rag_agent import ipo_answers
from app.agent.general_agent import general_agent_invoke


builder = StateGraph(AgentState)
# builder.add_node("define_ipo_answers", ipo_answers) #type:ignore
builder.add_node("define_ipo_answers", general_agent_invoke) #type:ignore
builder.add_edge(START, "define_ipo_answers")

memory = MemorySaver()
agentic_flow = builder.compile(checkpointer=memory)
