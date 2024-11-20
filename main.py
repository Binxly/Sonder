import time

from swarm import Swarm

from src.agents import agent_one, agent_two
from src.config import COST_PRINT_INTERVAL, INITIAL_BUDGET, MAX_HISTORY
from src.config import client as openai_client
from src.ui import (
    console,
    print_agent_message,
    print_final_summary,
    print_start,
    print_status_update,
)
from src.utils import calculate_cost, format_history

client = Swarm(client=openai_client)


def handle_agent_turn(
    agent,
    context_variables,
    conversation_history,
    agent_number,
    color,
    current_cost,
):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a more focused message structure
    messages = [
        {"role": "system", "content": "Speak freely and naturally, responding to the previous message if there is one."}
    ]
    
    # Add the last message from the other agent if it exists
    if conversation_history:
        messages.append(conversation_history[-1])
    
    # Update context variables with formatted history for reference
    context_variables["conversation_history"] = format_history(conversation_history)
    
    response = client.run(
        agent=agent,
        messages=messages,
        context_variables=context_variables,
    )
    latest_message = response.messages[-1]
    new_cost = current_cost + calculate_cost([latest_message])

    conversation_history.append(latest_message)
    print_agent_message(latest_message, agent_number, current_time, color)

    return new_cost


def check_cost_status(last_print_time, agent_1_cost, agent_2_cost):
    current_time = time.time()
    if current_time - last_print_time >= COST_PRINT_INTERVAL:
        print_status_update(
            {"agent_1": INITIAL_BUDGET, "agent_2": INITIAL_BUDGET},
            {"agent_1": agent_1_cost, "agent_2": agent_2_cost},
        )
        return current_time
    return last_print_time


def main():
    conversation_history = []
    context_variables = {
        "agent_1_budget": INITIAL_BUDGET,
        "agent_2_budget": INITIAL_BUDGET,
        "conversation_history": "",
    }

    agent_1_cost = agent_2_cost = 0.0
    print_start()
    last_cost_print = time.time()

    try:
        while True:
            if (
                agent_1_cost > context_variables["agent_1_budget"]
                or agent_2_cost > context_variables["agent_2_budget"]
            ):
                console.print(f"\nExperiment concluded: Budget depleted")
                console.print(f"Agent 1 spent: ${agent_1_cost:.4f}")
                console.print(f"Agent 2 spent: ${agent_2_cost:.4f}")
                break

            context_variables.update(
                {
                    "current_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "conversation_history": (
                        f"Recent conversation history:\n{format_history(conversation_history)}\n\n"
                        if conversation_history
                        else ""
                    ),
                }
            )

            # Agent turns
            agent_1_cost = handle_agent_turn(
                agent_one,
                context_variables,
                conversation_history,
                1,
                "cyan",
                agent_1_cost,
            )
            last_cost_print = check_cost_status(
                last_cost_print, agent_1_cost, agent_2_cost
            )

            agent_2_cost = handle_agent_turn(
                agent_two,
                context_variables,
                conversation_history,
                2,
                "green",
                agent_2_cost,
            )
            last_cost_print = check_cost_status(
                last_cost_print, agent_1_cost, agent_2_cost
            )

    except KeyboardInterrupt:
        console.print("\n[bold red]Experiment terminated by observer.[/bold red]")
    finally:
        print_final_summary({"agent_1": agent_1_cost, "agent_2": agent_2_cost})


if __name__ == "__main__":
    main()
