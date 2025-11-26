"""Query Generator Agent - Generates SQL query based on extracted information"""

import pickle
from agents.query_generator_agents.generate_query_chain import generate_sql_query_chain


def query_generator_agent(state):
    """Generate SQL query based on user query, subquestions, selected columns, and filters"""
    print(f"[AGENT] Invoking SQL QUERY GENERATOR AGENT")
    print(f"[AGENT] Selected columns: {len(state.selected_columns)} agent(s)")
    print(f"[AGENT] Filters: {state.filters}")
    
    try:
        # Load table schema from knowledgebase metadata
        with open('knowledgebase_metadata.pkl', 'rb') as f:
            metadata = pickle.load(f)
        
        # Build table schema from metadata
        table_schema = "\n".join([
            f"**{table_name}:**\n{description}"
            for table_name, description in metadata.items()
        ])
        
        print(f"[AGENT] Schema loaded: {len(metadata)} table(s)")
        
        # Flatten selected_columns: combine all column values from all agents
        all_selected_columns = []
        for agent_name, columns in state.selected_columns.items():
            all_selected_columns.extend(columns)
        
        print(f"[AGENT] Total selected columns: {len(all_selected_columns)}")
        
        # Invoke SQL generation chain
        sql_query = generate_sql_query_chain.invoke({
            "user_query": state.user_query,
            "selected_columns": str(all_selected_columns),
            "filters": str(state.filters),
            "table_schema": table_schema
        })
        
        state.generated_query = sql_query
        print(f"[AGENT] [SUCCESS] SQL Query Generator completed\n")
        print(f"[AGENT] ================================================================================")
        print(f"[AGENT] FINAL GENERATED QUERY:")
        print(f"[AGENT] {state.generated_query}")
        print(f"[AGENT] ================================================================================\n")
        
    except Exception as e:
        print(f"[AGENT] [ERROR] SQL Query Generator Error: {str(e)}\n")
        state.generated_query = ""
    
    return state
