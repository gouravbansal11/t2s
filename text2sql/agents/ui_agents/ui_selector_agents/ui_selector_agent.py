from agents.ui_agents.ui_selector_agents.ui_selector_agent_chain import ui_selector_agent_chain

def ui_selector_agent_impl(state): 
    """ Invoke the UI Selector Agent to determine UI components based on the user query and SQL Query Generated. """
    print(f"[UI SELECTOR AGENT] Invoking UI SELECTOR AGENT")
    print(f"[UI SELECTOR AGENT] User Query: {state.user_query}")

    # Invoke the chain to get UI component recommendation as JSON dictionary
    ui_selector_agent_chain_response = ui_selector_agent_chain.invoke({
        "user_query": state.user_query, 
        "generated_sql_query": state.generated_sql_query
    })

    print(f"[UI SELECTOR AGENT] [SUCCESS] UI Selector completed")
    print(f"[UI SELECTOR AGENT] |-- UI Selector response: \n{ui_selector_agent_chain_response}\n")

    # Extract recommended component from JSON response
    try:
        recommended_component = ui_selector_agent_chain_response.get("recommended_component", "table")
        fields = ui_selector_agent_chain_response.get("fields", [])
        configs = ui_selector_agent_chain_response.get("configs", {})
        print(f"[UI SELECTOR AGENT] |-- Recommended Component: {recommended_component}")    
    except (AttributeError, KeyError) as e:
        print(f"[UI SELECTOR AGENT] [WARNING] Failed to extract recommendation: {str(e)}")
        print(f"[UI SELECTOR AGENT] [INFO] Defaulting to 'table' component")
        recommended_component = "table"

    return {
        "ui_components": {"recommended_component": recommended_component, "fields": fields, "configs": configs}
    }