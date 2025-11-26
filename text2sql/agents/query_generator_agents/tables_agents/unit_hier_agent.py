"""Unit Hierarchy Agent - Extracts tables and columns relevant to unit hierarchy queries"""

from agents.query_generator_agents.table_extractor.TableExtractorAgent import table_extractor_graph, TableExtractorState


def unit_hier_agent(state, table_dict):
    """Extract tables and columns relevant to unit hierarchy queries"""
    print(f"\n[AGENT] Invoking UNIT HIERARCHY AGENT")
    print(f"[AGENT] Tables to analyze: {table_dict.get('unit_hier_agent')}")
    
    try:
        unit_hier_agent_response = table_extractor_graph.invoke(
            TableExtractorState(
                user_query=state.user_query, 
                table_list=table_dict.get("unit_hier_agent")
            )
        )
        
        subquestions_result = unit_hier_agent_response.get("subquestion_extractor_response", [])
        columns_result = unit_hier_agent_response.get("selected_columns", [])
        
        print(f"[AGENT] [SUCCESS] Unit Hierarchy Agent completed")
        print(f"[AGENT]   |-- Subquestions: {len(subquestions_result)}")
        print(f"[AGENT]   |-- Selected columns: {len(columns_result)}\n")
        
        # Return updates - reducer will merge with concurrent updates
        return {
            "subquestions": {"unit_hier_agent": subquestions_result},
            "selected_columns": {"unit_hier_agent": columns_result}
        }
    except Exception as e:
        print(f"[AGENT] [ERROR] Unit Hierarchy Agent Error: {str(e)}\n")
        raise
