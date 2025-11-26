"""Project Agent - Extracts tables and columns relevant to project queries"""

from agents.query_generator_agents.table_extractor.TableExtractorAgent import table_extractor_graph, TableExtractorState


def project_agent(state, table_dict):
    """Extract tables and columns relevant to project queries"""
    print(f"[AGENT] Invoking PROJECT AGENT")
    print(f"[AGENT] Tables to analyze: {table_dict.get('project_agent')}")
    
    try:
        project_agent_response = table_extractor_graph.invoke(
            TableExtractorState(
                user_query=state.user_query, 
                table_list=table_dict.get("project_agent")
            )
        )
        
        subquestions_result = project_agent_response.get("subquestion_extractor_response", [])
        columns_result = project_agent_response.get("selected_columns", [])
        
        print(f"[AGENT] [SUCCESS] Project Agent completed")
        print(f"[AGENT]   |-- Subquestions: {len(subquestions_result)}")
        print(f"[AGENT]   |-- Selected columns: {len(columns_result)}\n")
        
        # Return updates - reducer will merge with concurrent updates
        return {
            "subquestions": {"project_agent": subquestions_result},
            "selected_columns": {"project_agent": columns_result}
        }
    except Exception as e:
        print(f"[AGENT] [ERROR] Project Agent Error: {str(e)}\n")
        raise
