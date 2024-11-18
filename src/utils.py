from .config import COST_PER_TOKEN, model

def calculate_cost(messages: list) -> float:
    input_tokens = sum(len(str(m.get("content", ""))) / 4 for m in messages if m["role"] != "assistant")
    output_tokens = sum(len(str(m.get("content", ""))) / 4 for m in messages if m["role"] == "assistant")
    
    return (input_tokens * COST_PER_TOKEN[model]["input"]) + \
           (output_tokens * COST_PER_TOKEN[model]["output"])

def format_history(conversation_history):
    return "\n".join([
        f"{'Agent 1' if idx % 2 == 0 else 'Agent 2'}: {msg['content']}"
        for idx, msg in enumerate(conversation_history[-10:])
    ]) 