from pydantic import BaseModel
from typing import Annotated
from agents.router_agent import router_agent, get_available_agents, get_agent_tables
#from agents.ui_agents.ui_selector_agents.ui_selector_agent import ui_selector_agent_impl
from langgraph.graph import StateGraph, START, END
from utils.stateReducers import merge_dicts
from utils.db_utility import execute_query

# Import table extraction agents
from agents.query_generator_agents.tables_agents import (
    unit_hier_agent as unit_hier_agent_impl,
    project_agent as project_agent_impl,
    dimension_agent as dimension_agent_impl,
    filter_check_agent as filter_check_agent_impl,
)

# Import query generator agents
from agents.query_generator_agents import query_generator_agent as query_generator_agent_impl

# Get agent configuration from router agent (single source of truth)
sql_agents = get_available_agents()
table_dict = get_agent_tables()


class AgentState(BaseModel):
    user_query: str = ""
    router_response: list[str] = []
    subquestions: Annotated[dict, merge_dicts] = {}  # ✅ Handles concurrent updates
    selected_columns: Annotated[dict, merge_dicts] = {}  # ✅ Handles concurrent updates
    filters: list = []  # Stores filter conditions
    generated_sql_query: str = ""  # Final SQL query
    ui_components_details: dict = {}  # Stores UI components


def router(state: AgentState):
    """Route query to appropriate agents based on keywords"""
    query = state.user_query
    print("\n" + "#" * 80)
    print("# [ORCHESTRATION] Starting Text-to-SQL Pipeline")
    print("#" * 80)
    print(f"[ORCHESTRATION] User Query: {query}\n")
    
    try:
        result = router_agent(query)
        mapped_agents = result.get('mapped_agents', [])
        state.router_response = mapped_agents
        print(f"[ORCHESTRATION] [SUCCESS] Routing complete: {mapped_agents}\n")
        return state
    except Exception as e:
        print(f"[ORCHESTRATION] [ERROR] Router Error: {str(e)}\n")
        raise


def router_request(state: AgentState):
    """Return router response for conditional edges"""
    return state.router_response


def unit_hier_agent(state: AgentState):
    """Wrapper for unit hierarchy agent"""
    return unit_hier_agent_impl(state, table_dict)


def project_agent(state: AgentState):
    """Wrapper for project agent"""
    return project_agent_impl(state, table_dict)


def dimension_agent(state: AgentState):
    """Wrapper for dimension agent"""
    return dimension_agent_impl(state, table_dict)


def filter_check_agent(state: AgentState):
    """Wrapper for filter check agent"""
    return filter_check_agent_impl(state)


def query_generator_agent(state: AgentState):
    """Wrapper for query generator agent"""
    return query_generator_agent_impl(state)


def ui_selector_agent(state):
    """Wrapper for UI Selector Agent"""
    return ui_selector_agent_impl(state)

def invoke_t2s_pipeline():
        # Build StateGraph
    state_graph = StateGraph(AgentState)
    state_graph.add_node("router", router)
    state_graph.add_node("unit_hier_agent", unit_hier_agent)
    state_graph.add_node("project_agent", project_agent)
    state_graph.add_node("dimension_agent", dimension_agent)
    state_graph.add_node("filter_check_agent", filter_check_agent)
    state_graph.add_node("query_generator_agent", query_generator_agent)
    state_graph.add_node("ui_selector_agent", ui_selector_agent)

    state_graph.add_edge(START, "router")
    state_graph.add_conditional_edges("router", router_request, sql_agents)
    state_graph.add_edge("unit_hier_agent", "filter_check_agent")
    state_graph.add_edge("project_agent", "filter_check_agent")
    state_graph.add_edge("dimension_agent", "filter_check_agent")
    state_graph.add_edge("filter_check_agent", "query_generator_agent")
    state_graph.add_edge("query_generator_agent", "ui_selector_agent")
    state_graph.add_edge("ui_selector_agent", END)

    state_graph_final = state_graph.compile()

    # Execute pipeline
    print("\n" + "=" * 80)
    print("TEXT-TO-SQL CONVERSION PIPELINE")
    print("=" * 80 + "\n")

    result = state_graph_final.invoke(AgentState(user_query=input("Enter the query: ")))

    print("\n" + "=" * 80)
    print(f"PIPELINE EXECUTION COMPLETED. RESULT: {result}")
    print("=" * 80 + "\n")
    return result

#from services.ui_generator import generate_ui

def draw_data(state: AgentState):
    # Placeholder for drawing or exporting pipeline results; implement as needed
    data = execute_query(state["generated_sql_query"])
    print(f"Data retrieved from database: {data}")
    ui_components_details = state["ui_components_details"]
 #   generate_ui(ui_components_details.get("recommended_component"), ui_components_details.get("fields", []),ui_components_details.get("configs", {}), data)
    

def main():
    final_state = invoke_t2s_pipeline()
    draw_data(state=final_state)

main()

