from pydantic_ai.messages import ModelRequest, UserPromptPart
from datetime import datetime, timezone

# Convert LangGraph's HumanMessage to ModelRequest (for user messages)
def convert_human_message_to_model_message(human_messages):
    model_messages = []
    
    for msg in human_messages:
        model_messages.append(
            ModelRequest(
                        parts=[
                                UserPromptPart(
                                                content=msg.content, 
                                                timestamp=datetime.now(timezone.utc)
                                                )
                                ]
            )
        )
    
    return model_messages