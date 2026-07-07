"""
Elitze Sentinel Frontier — LangGraph Agent

Five-phase agentic pipeline:
1. Ingest — Parse and normalize user input
2. Recon — Gather context and dependencies
3. Interview — Extract intent and requirements
4. Compile — Generate executable plan
5. Handoff — Execute and return results

Supports both base (no LLM) and LLM-enhanced modes.
"""

from typing import Any, Dict, Optional
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel


class AgentState(BaseModel):
    """State object passed through the graph."""

    input: str
    phase: str = "ingest"
    context: Dict[str, Any] = {}
    plan: Optional[str] = None
    result: Optional[str] = None


def ingest_phase(state: AgentState) -> AgentState:
    """Phase 1: Parse and normalize user input."""
    print(f"[Phase 1] Ingest: {state.input}")
    state.phase = "ingest"
    state.context["raw_input"] = state.input
    state.context["normalized"] = state.input.lower().strip()
    return state


def recon_phase(state: AgentState) -> AgentState:
    """Phase 2: Gather context and dependencies."""
    print(f"[Phase 2] Recon")
    state.phase = "recon"
    state.context["dependencies"] = []
    state.context["scope"] = "local"
    return state


def interview_phase(state: AgentState) -> AgentState:
    """Phase 3: Extract intent and requirements."""
    print(f"[Phase 3] Interview")
    state.phase = "interview"
    state.context["intent"] = "process"
    state.context["requirements"] = []
    return state


def compile_phase(state: AgentState) -> AgentState:
    """Phase 4: Generate executable plan."""
    print(f"[Phase 4] Compile")
    state.phase = "compile"
    state.plan = f"Execute: {state.context.get('normalized', 'unknown')}"
    return state


def handoff_phase(state: AgentState) -> AgentState:
    """Phase 5: Execute and return results."""
    print(f"[Phase 5] Handoff")
    state.phase = "handoff"
    state.result = f"Completed: {state.plan}"
    return state


def create_fable5_graph():
    """Create the base five-phase LangGraph agent."""
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("ingest", ingest_phase)
    graph.add_node("recon", recon_phase)
    graph.add_node("interview", interview_phase)
    graph.add_node("compile", compile_phase)
    graph.add_node("handoff", handoff_phase)

    # Add edges (linear pipeline)
    graph.add_edge(START, "ingest")
    graph.add_edge("ingest", "recon")
    graph.add_edge("recon", "interview")
    graph.add_edge("interview", "compile")
    graph.add_edge("compile", "handoff")
    graph.add_edge("handoff", END)

    return graph.compile()


def create_fable5_graph_with_llm(llm=None):
    """
    Create an LLM-enhanced version of the five-phase agent.

    Args:
        llm: Optional LLM instance (Anthropic, OpenAI, or local).
             If None, attempts to auto-detect from environment.

    Returns:
        Compiled LangGraph with LLM-enhanced nodes.
    """
    if llm is None:
        # Auto-detect LLM from environment
        try:
            from langchain_anthropic import ChatAnthropic

            llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
        except ImportError:
            try:
                from langchain_openai import ChatOpenAI

                llm = ChatOpenAI(model="gpt-4o-mini")
            except ImportError:
                raise RuntimeError(
                    "No LLM available. Install langchain-anthropic or langchain-openai."
                )

    def llm_ingest(state: AgentState) -> AgentState:
        """LLM-enhanced ingest: parse intent."""
        print(f"[Phase 1 + LLM] Ingest")
        state.phase = "ingest"
        state.context["raw_input"] = state.input
        # In a real implementation, use LLM to extract structured intent
        state.context["normalized"] = state.input.lower().strip()
        return state

    def llm_interview(state: AgentState) -> AgentState:
        """LLM-enhanced interview: extract requirements."""
        print(f"[Phase 3 + LLM] Interview")
        state.phase = "interview"
        # In a real implementation, use LLM to extract requirements
        state.context["intent"] = "process"
        state.context["requirements"] = []
        return state

    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("ingest", llm_ingest)
    graph.add_node("recon", recon_phase)
    graph.add_node("interview", llm_interview)
    graph.add_node("compile", compile_phase)
    graph.add_node("handoff", handoff_phase)

    # Add edges
    graph.add_edge(START, "ingest")
    graph.add_edge("ingest", "recon")
    graph.add_edge("recon", "interview")
    graph.add_edge("interview", "compile")
    graph.add_edge("compile", "handoff")
    graph.add_edge("handoff", END)

    return graph.compile()

