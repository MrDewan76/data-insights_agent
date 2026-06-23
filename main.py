# This is the file you actually run. Its job is small on purpose: show a
# welcome message, take whatever the user types, hand it to the
# Orchestrator, and print whatever comes back. It doesn't know anything
# about World Bank data, agents, or APIs — all of that lives in the other files.

import os
import sys
import anthropic
from agents.orchestrator import Orchestrator


def main():
    # We need your Anthropic API key to talk to Claude at all. We read it
    # from an environment variable rather than writing it directly in the
    # code, so you never accidentally commit your key to GitHub.
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: Set the ANTHROPIC_API_KEY environment variable first.")
        print("  export ANTHROPIC_API_KEY=your-key-here")
        sys.exit(1)

    # One client connects to Claude, one Orchestrator manages the whole
    # conversation. Both get created once, right here, and then reused
    # for every message in the loop below.
    client = anthropic.Anthropic(api_key=api_key)
    orchestrator = Orchestrator(client)

    print("=" * 60)
    print("  Data Insights Agent — World Bank Economic Data")
    print("  Multi-agent architecture: Orchestrator -> Query -> Analysis")
    print("=" * 60)
    print("\nAsk about GDP, population, inflation, unemployment, life")
    print("expectancy, and more — for any country, live from the World Bank.")
    print("\nExamples:")
    print('  "Compare GDP growth in India and Brazil from 2015 to 2023"')
    print('  "What\'s the unemployment trend in Germany over the last decade?"')
    print('  "Now show that as a percentage of GDP instead"  (follow-up)')
    print("\nType 'quit' to exit.\n")

    # This is the main loop: keep asking for input until the user quits.
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            break

        print("\nAgent: thinking...\n")

        # This single line is where everything else in the project
        # actually gets used. handle_message() is defined in
        # agents/orchestrator.py, and from here it's the orchestrator's
        # job to figure out the rest.
        response = orchestrator.handle_message(user_input)

        print(f"Agent: {response}\n")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
