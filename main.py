#!/usr/bin/env python3
"""
Elitze Sentinel Frontier — Python Agent Entrypoint

Runs the LangGraph agent with optional LLM enhancement.
Usage:
  python main.py "your prompt"
  python main.py "your prompt" --llm
"""

import sys
import argparse
from agent.graph import create_fable5_graph, create_fable5_graph_with_llm


def main():
    parser = argparse.ArgumentParser(
        description="Elitze Sentinel Frontier — LangGraph Agent"
    )
    parser.add_argument("prompt", help="Input prompt for the agent")
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Enable LLM-enhanced processing (requires ANTHROPIC_API_KEY or OPENAI_API_KEY)",
    )

    args = parser.parse_args()

    # Create the appropriate graph
    if args.llm:
        print("[*] Creating LLM-enhanced graph...")
        graph = create_fable5_graph_with_llm()
    else:
        print("[*] Creating base graph...")
        graph = create_fable5_graph()

    # Run the agent
    print(f"[*] Processing prompt: {args.prompt}\n")
    try:
        result = graph.invoke({"input": args.prompt})
        print("\n[✓] Agent execution complete")
        print(f"Result: {result}")
    except Exception as e:
        print(f"[✗] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

