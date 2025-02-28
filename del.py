from pydantic_ai import Agent
from dotenv import load_dotenv
load_dotenv()
agent = Agent('openai:gpt-4o-mini', system_prompt='Be a helpful assistant.')
# user_inputs = ["Hi there! My name is Will.", "What is my name?"]

result1 = agent.run_sync('Hi there! My name is Will.')
print(f"printing messages {result1.new_messages()}")
result2 = agent.run_sync('What is my name?', message_history=result1.new_messages())
print(result2.data)


# from typing import Annotated

# from langchain_core.messages import BaseMessage
# from typing_extensions import TypedDict
# from langchain_openai import ChatOpenAI
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import StateGraph, START
# from langgraph.graph.message import add_messages
# from langgraph.prebuilt import ToolNode

# memory = MemorySaver()

# class State(TypedDict):
#     messages: Annotated[list, add_messages]

# llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18")
# def chatbot(state: State):
#     if not isinstance(ls, list):
#         ls = [ls]  # Convert to list if it's a single object
#     ls= state.get("messages", [])

#     message_history = [msg.content for msg in ls]

#     print(f"LS -> {message_history}")
#     print(f"LS 1-> {message_history[0]}")
#     return {"messages": [llm.invoke(state["messages"])]}

# graph_builder = StateGraph(State)
# # The first argument is the unique node name
# # The second argument is the function or object that will be called whenever
# # the node is used.
# graph_builder.add_node("chatbot", chatbot)
# graph_builder.set_entry_point("chatbot")
# graph_builder.set_finish_point("chatbot")
# graph = graph_builder.compile(checkpointer=memory)

# config = {"configurable": {"thread_id": "1"}}


# user_inputs = ["Hi there! My name is Will.", "What is my name?"]

# for user_input in user_inputs:
#     # The config is the **second positional argument** to stream() or invoke()!
#     events = graph.stream(
#         {"messages": [{"role": "user", "content": user_input}]},
#         config,  # type: ignore
#         stream_mode="values",
#     )

#     for event in events:

#         event["messages"][-1].pretty_print()
