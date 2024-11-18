# Sonder: Swarm Chat

Lets AI agents chat with each other using the Swarm framework. They'll keep talking until they run out of a budget you set, or you stop them. Occasional budget updates are printed to the console.

- Tracks token costs for each agent
- Pretty Printing
- Keeps a bit of theconversation history for context

## Setup

1. Clone the repo
2. Copy `.env.example` to `.env`, and add your OpenAI key.
3. Run `pip install git+https://github.com/openai/swarm.git` to install [Swarm](https://github.com/openai/swarm)
4. Run `pip install -r requirements.txt`
5. Run `python main.py`
