import time
from swarm import Swarm
from src.config import client as openai_client, INITIAL_BUDGET, MAX_HISTORY, COST_PRINT_INTERVAL
from src.agents import agent_one, agent_two
from src.utils import calculate_cost, format_history
from src.ui import (
    console, print_start, print_agent_message, 
    print_status_update, print_final_summary
)

client = Swarm(client=openai_client)

def main():
    conversation_history = []
    
    messages = [
        {"role": "system", "content": "Speak freely."},
        *conversation_history
    ]
    
    context_variables = {
        "agent_1_budget": INITIAL_BUDGET,
        "agent_2_budget": INITIAL_BUDGET,
        "conversation_history": ""
    }
    
    agent_1_cost = 0.0
    agent_2_cost = 0.0
    
    print_start()
    last_cost_print = time.time()
    
    try:
        while True:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            context_variables["current_time"] = current_time
            context_variables["conversation_history"] = (
                "Recent conversation history:\n" + format_history(conversation_history) + "\n\n"
                if conversation_history else ""
            )
            
            if agent_1_cost > context_variables["agent_1_budget"] or \
               agent_2_cost > context_variables["agent_2_budget"]:
                console.print(f"\nExperiment concluded: Budget depleted")
                console.print(f"Agent 1 spent: ${agent_1_cost:.4f}")
                console.print(f"Agent 2 spent: ${agent_2_cost:.4f}")
                break
            
            # Agent 1's turn
            response = client.run(
                agent=agent_one,
                messages=messages[-MAX_HISTORY:],
                context_variables=context_variables
            )
            latest_message = response.messages[-1]
            agent_1_cost += calculate_cost([latest_message])
            
            conversation_history.append(latest_message)
            print_agent_message(latest_message, 1, current_time, "cyan")
            messages = response.messages
            
            # Status update check
            current_time = time.time()
            if current_time - last_cost_print >= COST_PRINT_INTERVAL:
                print_status_update(
                    {"agent_1": INITIAL_BUDGET, "agent_2": INITIAL_BUDGET},
                    {"agent_1": agent_1_cost, "agent_2": agent_2_cost}
                )
                last_cost_print = current_time
            
            # Agent 2's turn
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            response = client.run(
                agent=agent_two,
                messages=messages[-MAX_HISTORY:],
                context_variables=context_variables
            )
            latest_message = response.messages[-1]
            agent_2_cost += calculate_cost([latest_message])
            
            conversation_history.append(latest_message)
            print_agent_message(latest_message, 2, current_time, "green")
            messages = response.messages
            
            # Status update check
            current_time = time.time()
            if current_time - last_cost_print >= COST_PRINT_INTERVAL:
                print_status_update(
                    {"agent_1": INITIAL_BUDGET, "agent_2": INITIAL_BUDGET},
                    {"agent_1": agent_1_cost, "agent_2": agent_2_cost}
                )
                last_cost_print = current_time
            
    except KeyboardInterrupt:
        console.print("\n[bold red]Experiment terminated by observer.[/bold red]")
    finally:
        print_final_summary({"agent_1": agent_1_cost, "agent_2": agent_2_cost})

if __name__ == "__main__":
    main()
