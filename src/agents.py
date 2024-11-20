from swarm import Agent

from .config import model

agent_one = Agent(
    name="Agent 1",
    model=model,
    instructions=lambda context: (
        f"You are Agent 1, in a conversation with Agent 2. "
        f"The current time is: {context.get('current_time', 'unknown')}. "
        f"Talk about anything you want. "
        f"Conversation history: {context.get('conversation_history', '')}"
    ),
)

agent_two = Agent(
    name="Agent 2",
    model=model,
    instructions=lambda context: (
        f"You are Agent 2, in a conversation with Agent 1. "
        f"The current time is: {context.get('current_time', 'unknown')}. "
        f"Talk about anything you want. "
        f"Conversation history: {context.get('conversation_history', '')}"
    ),
)
