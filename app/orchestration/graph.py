"""LangGraph execution engine for Project Fifty MVP."""
from __future__ import annotations

import logging
import time
from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END

from app.orchestration.factory import agent_factory

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """The shared state passed between nodes in the graph."""
    location: str
    query: str
    prior_context: dict
    selected_agent_names: list[str]
    current_agent_index: int
    accumulated_context: str
    results: list[dict]
    final_report: str
    error: Optional[str]


def run_agent_node(state: AgentState) -> dict:
    """Executes the current agent in the sequence."""
    idx = state["current_agent_index"]
    agent_name = state["selected_agent_names"][idx]
    
    logger.info("[%d/%d] Running agent: %s", idx + 1, len(state["selected_agent_names"]), agent_name)
    
    agents = agent_factory.build_by_names([agent_name])
    if not agents:
        logger.error("Failed to build agent: %s", agent_name)
        return {
            "current_agent_index": idx + 1,
            "error": f"Agent {agent_name} not found."
        }
        
    agent = agents[0]
    
    n = len(state["selected_agent_names"])
    if idx == 0 and n >= 2:
        task_desc = (
            f"Analyse this climate intelligence request and create an execution plan.\n\n"
            f"Location: {state['location']}\nQuery: {state['query']}\n"
            f"Prior context: {state['prior_context']}\n\n"
            f"Identify which specialist analyses are needed and in what order."
        )
    elif idx == n - 1:
        task_desc = (
            f"Generate a comprehensive climate intelligence report for {state['location']}.\n\n"
            f"Compile all preceding findings into a well-structured report.\n"
            f"Original query: {state['query']}\n\n"
            f"Include: executive summary, methodology, detailed findings, risk assessment, recommendations."
        )
    elif idx == n - 2 and n >= 3:
        task_desc = (
            f"Synthesise all preceding agent outputs into a single coherent decision for {state['location']}.\n\n"
            f"Produce: 1) Risk level, 2) Confidence score, 3) Key findings, 4) Top 5 recommendations."
        )
    else:
        task_desc = (
            f"You are contributing to a climate intelligence analysis for {state['location']}.\n\n"
            f"Original query: {state['query']}\n\n"
            f"Use your expertise to analyse relevant data and provide findings for your area of specialty."
        )

    t0 = time.time()
    output = agent.run(
        task_description=task_desc,
        context=state["accumulated_context"],
        location=state["location"],
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    
    logger.info("  → %s completed in %d ms", agent.name, elapsed_ms)

    new_result = {
        "agent": agent.name,
        "role": agent.role,
        "output": output,
        "elapsed_ms": str(elapsed_ms),
    }

    new_context = state["accumulated_context"] + f"\n\n[{agent.name}]:\n{output}"

    return {
        "current_agent_index": idx + 1,
        "accumulated_context": new_context,
        "results": state["results"] + [new_result],
    }


def compile_report_node(state: AgentState) -> dict:
    """Compiles the final report from all agent results."""
    logger.info("Compiling final report.")
    
    if state.get("error"):
        return {"final_report": f"Pipeline failed: {state['error']}"}

    final_parts = []
    for r in state["results"]:
        final_parts.append(f"## {r['agent']} ({r['role']})\n\n{r['output']}")
    
    combined = "\n\n---\n\n".join(final_parts)
    return {"final_report": combined}


def router(state: AgentState) -> str:
    """Determines whether to run the next agent or finish the pipeline."""
    if state.get("error"):
        return "compile_report"
        
    if state["current_agent_index"] < len(state["selected_agent_names"]):
        return "run_agent"
    return "compile_report"


# Build the Graph
builder = StateGraph(AgentState)

builder.add_node("run_agent", run_agent_node)
builder.add_node("compile_report", compile_report_node)

# Set the entry point
builder.set_entry_point("run_agent")

# Add conditional edges from run_agent
builder.add_conditional_edges(
    "run_agent",
    router,
    {
        "run_agent": "run_agent",
        "compile_report": "compile_report",
    }
)

# After compiling the report, the pipeline ends
builder.add_edge("compile_report", END)

climate_graph = builder.compile()
