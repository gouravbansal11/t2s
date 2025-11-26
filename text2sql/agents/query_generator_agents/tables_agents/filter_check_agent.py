"""Filter Check Agent - Checks for filter requirements based on selected columns"""

from agents.query_generator_agents.filter_check_agent.filter_check_chain import check_filter_agent_chain


def filter_check_agent(state):
    """Check for filter requirements based on selected columns and user query"""
    print(f"[AGENT] Invoking FILTER CHECK AGENT")
    
    # Combine all selected columns from all agents
    all_columns = []
    for agent_name, columns in state.selected_columns.items():
        all_columns.extend(columns)
    
    print(f"[AGENT] Total columns available for filtering: {len(all_columns)}")
    
    if all_columns:
        try:
            filter_result = check_filter_agent_chain.invoke({
                "user_query": state.user_query,
                "columns": str(all_columns)
            })
            import ast
            state.filters = ast.literal_eval(filter_result) if filter_result else []
            print(f"[AGENT] [SUCCESS] Filter Check completed")
            print(f"[AGENT]   |-- Filters applied: {state.filters}\n")
        except Exception as e:
            print(f"[AGENT] [ERROR] Filter Check Error: {str(e)}")
            state.filters = []
    else:
        print(f"[AGENT] [INFO] No columns selected - skipping filter check")
        state.filters = []
    
    return state
