from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    latest_user_message:Annotated[list, add_messages]
    # messages: Annotated[List[bytes], lambda x, y: x + y]

