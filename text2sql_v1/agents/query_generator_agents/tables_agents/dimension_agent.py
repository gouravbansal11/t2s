"""Dimension Agent - Extracts dimension tables for lookup and enrichment"""

from agents.query_generator_agents.table_extractor.TableExtractorAgent import table_extractor_graph, TableExtractorState


def dimension_agent(state, table_dict):
    """Extract dimension tables for lookup and enrichment"""
    print(f"[AGENT] Invoking DIMENSION AGENT")
    print(f"[AGENT] Tables to analyze: {table_dict.get('dimension_agent')}")
    
    try:
        dimension_agent_response = table_extractor_graph.invoke(
            TableExtractorState(
                user_query=state.user_query, 
                table_list=table_dict.get("dimension_agent")
            )
        )
        
        subquestions_result = dimension_agent_response.get("subquestion_extractor_response", [])
        columns_result = dimension_agent_response.get("selected_columns", [])
        
        print(f"[AGENT] [SUCCESS] Dimension Agent completed")
        print(f"[AGENT]   |-- Subquestions: {len(subquestions_result)}")
        print(f"[AGENT]   |-- Selected columns: {len(columns_result)}\n")
        
        return {
            "subquestions": {"dimension_agent": subquestions_result},
            "selected_columns": {"dimension_agent": columns_result}
        }
    except Exception as e:
        print(f"[AGENT] [ERROR] Dimension Agent Error: {str(e)}\n")
        raise
