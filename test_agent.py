"""
Elitze Sentinel Frontier — Agent Tests

Run with: pytest test_agent.py -v
"""

import pytest
from agent.graph import (
    AgentState,
    create_fable5_graph,
    create_fable5_graph_with_llm,
    ingest_phase,
    recon_phase,
    interview_phase,
    compile_phase,
    handoff_phase,
)


class TestAgentPhases:
    """Test individual agent phases."""

    def test_ingest_phase(self):
        """Test ingest phase normalizes input."""
        state = AgentState(input="Test Prompt")
        result = ingest_phase(state)
        assert result.phase == "ingest"
        assert result.context["raw_input"] == "Test Prompt"
        assert result.context["normalized"] == "test prompt"

    def test_recon_phase(self):
        """Test recon phase initializes context."""
        state = AgentState(input="test", context={"raw_input": "test"})
        result = recon_phase(state)
        assert result.phase == "recon"
        assert "dependencies" in result.context
        assert result.context["scope"] == "local"

    def test_interview_phase(self):
        """Test interview phase extracts intent."""
        state = AgentState(input="test", context={})
        result = interview_phase(state)
        assert result.phase == "interview"
        assert result.context["intent"] == "process"
        assert "requirements" in result.context

    def test_compile_phase(self):
        """Test compile phase generates plan."""
        state = AgentState(input="test", context={"normalized": "test"})
        result = compile_phase(state)
        assert result.phase == "compile"
        assert result.plan is not None
        assert "Execute" in result.plan

    def test_handoff_phase(self):
        """Test handoff phase produces result."""
        state = AgentState(input="test", plan="Execute: test")
        result = handoff_phase(state)
        assert result.phase == "handoff"
        assert result.result is not None
        assert "Completed" in result.result


class TestGraphs:
    """Test graph creation and execution."""

    def test_base_graph_creation(self):
        """Test base graph compiles without errors."""
        graph = create_fable5_graph()
        assert graph is not None

    def test_base_graph_execution(self):
        """Test base graph executes end-to-end."""
        graph = create_fable5_graph()
        initial_state = AgentState(input="test prompt")
        result = graph.invoke(initial_state)

        assert result.phase == "handoff"
        assert result.result is not None
        assert result.plan is not None
        assert result.context["normalized"] == "test prompt"

    def test_llm_graph_creation(self):
        """Test LLM-enhanced graph compiles without errors."""
        try:
            graph = create_fable5_graph_with_llm()
            assert graph is not None
        except RuntimeError as e:
            # Expected if no LLM is configured
            assert "No LLM available" in str(e)

    def test_graph_state_flow(self):
        """Test state flows through all phases."""
        graph = create_fable5_graph()
        initial_state = AgentState(input="complex task")
        result = graph.invoke(initial_state)

        # Verify all phases were executed
        assert result.context["raw_input"] == "complex task"
        assert result.context["normalized"] == "complex task"
        assert result.context["scope"] == "local"
        assert result.context["intent"] == "process"
        assert result.plan is not None
        assert result.result is not None


class TestAgentState:
    """Test AgentState model."""

    def test_state_initialization(self):
        """Test state initializes with defaults."""
        state = AgentState(input="test")
        assert state.input == "test"
        assert state.phase == "ingest"
        assert state.context == {}
        assert state.plan is None
        assert state.result is None

    def test_state_with_context(self):
        """Test state accepts context."""
        context = {"key": "value"}
        state = AgentState(input="test", context=context)
        assert state.context == context

