from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_start():
    console.print(Panel.fit(
        Text("AI Dialogue Experiment", style="bold magenta"),
        subtitle="Observing ..."
    ))
    console.print("Press Ctrl+C to terminate the experiment\n")

def print_agent_message(message, agent_num, current_time, color):
    console.print(Panel(
        Markdown(message['content'], style=color),
        title=f"[{current_time}] Agent {agent_num}",
        border_style=color,
        padding=(1, 2)
    ))

def print_status_update(budgets, costs):
    remaining_1 = budgets["agent_1"] - costs["agent_1"]
    remaining_2 = budgets["agent_2"] - costs["agent_2"]
    
    console.print(Panel(
        Text(
            f"Starting Budget: ${budgets['agent_1']:.4f} / ${budgets['agent_2']:.4f}\n"
            f"Agent 1 spent: ${costs['agent_1']:.4f} (Remaining: ${remaining_1:.4f})\n"
            f"Agent 2 spent: ${costs['agent_2']:.4f} (Remaining: ${remaining_2:.4f})",
            style="bold yellow",
            justify="center"
        ),
        title="Status Update",
        border_style="yellow",
        padding=(1, 2)
    ))

def print_final_summary(costs):
    console.print(Panel(
        f"Agent 1 total cost: ${costs['agent_1']:.4f}\n"
        f"Agent 2 total cost: ${costs['agent_2']:.4f}",
        style="bold yellow"
    )) 