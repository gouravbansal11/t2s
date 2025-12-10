from langgraph.graph import StateGraph,START,END
from pydantic import BaseModel
import pickle

from agents.query_generator_agents.table_extractor.SubQueryExtractorChain import generate_subquestions_chain
from agents.query_generator_agents.table_extractor.ColumnExtractorChain import generate_columnExtractor_chain

class TableExtractorState(BaseModel):
    user_query: str
    agent_system_message: str = ""
    table_list: list[str]
    subquestion_extractor_response: list[list[str]] = []  # Default to an empty list
    selected_columns: list = []  # Store extracted columns

knowledgebase_metadata = {}

with open("knowledgebase_metadata.pkl","rb") as f:
   knowledgebase_metadata = pickle.load(f)

def subquestion_extractor(state: TableExtractorState) -> str:
    query = state.user_query
    tables = state.table_list
    print("\n" + "="*80)
    print("[TABLE EXTRACTOR - SUBQUESTION] Starting subquestion extraction")
    print("="*80)
    print(f"[TABLE EXTRACTOR - SUBQUESTION] User Query: {query}")
    print(f"[TABLE EXTRACTOR - SUBQUESTION] Tables to analyze: {tables}")
    
    # Check if metadata is available
    missing_tables = []
    table_desc = []
    
    for table in tables:
        if table in knowledgebase_metadata:
            desc = knowledgebase_metadata.get(table)
            preview = desc[:100] + "..." if len(str(desc)) > 100 else desc
            print(f"[TABLE EXTRACTOR - SUBQUESTION] Metadata for '{table}': {preview}")
            table_desc.append(table + ":" + desc)
        else:
            missing_tables.append(table)
            print(f"[TABLE EXTRACTOR - SUBQUESTION] [WARNING] Metadata for '{table}': No metadata found in knowledge base")
    
    # Check if any metadata was found
    if not table_desc:
        print(f"[TABLE EXTRACTOR - SUBQUESTION] [ERROR] No metadata found for any tables: {missing_tables}")
        print(f"[TABLE EXTRACTOR - SUBQUESTION] [ERROR] Cannot generate subquestions without table metadata")
        print(f"[TABLE EXTRACTOR - SUBQUESTION] [ERROR] Recommendation: Run knowledgebaseAgent.py to generate metadata")
        print("="*80 + "\n")
        state.subquestion_extractor_response = []
        return state
    
    if missing_tables:
        print(f"[TABLE EXTRACTOR - SUBQUESTION] [WARNING] Proceeding with {len(table_desc)} available table(s) out of {len(tables)}")
    
    print(f"[TABLE EXTRACTOR - SUBQUESTION] [SUCCESS] Loaded metadata for {len(table_desc)} table(s)")
    
    try:
        generate_subquestions_chain_res = generate_subquestions_chain.invoke({ "user_query": query, "table_desc": table_desc , "agent_system_message": state.agent_system_message })
        print(f"[TABLE EXTRACTOR - SUBQUESTION] LLM Response: {generate_subquestions_chain_res}")
        
        # Parse the response safely
        try:
            parsed_response = eval(generate_subquestions_chain_res)
        except (ValueError, SyntaxError) as e:
            print(f"[TABLE EXTRACTOR - SUBQUESTION] [ERROR] Failed to parse LLM response as list: {str(e)}")
            print(f"[TABLE EXTRACTOR - SUBQUESTION] [ERROR] Raw response: {generate_subquestions_chain_res}")
            parsed_response = []
        
        # Filter out empty subquestion groups [[]]
        state.subquestion_extractor_response = [sq for sq in parsed_response if sq and sq != []]
        
        if not state.subquestion_extractor_response:
            print(f"[TABLE EXTRACTOR - SUBQUESTION] [WARNING] No valid subquestions generated from user query")
            print(f"[TABLE EXTRACTOR - SUBQUESTION] [WARNING] This may mean: user query is too broad, too vague, or doesn't require table filtering")
        else:
            print(f"[TABLE EXTRACTOR - SUBQUESTION] Parsed subquestions: {state.subquestion_extractor_response}")
        
        print(f"[TABLE EXTRACTOR - SUBQUESTION] [SUCCESS] Subquestion extraction completed ({len(state.subquestion_extractor_response)} valid subquestion(s))")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"[TABLE EXTRACTOR - SUBQUESTION] [ERROR] Error during LLM invocation: {str(e)}")
        print(f"[TABLE EXTRACTOR - SUBQUESTION] [ERROR] Stack trace: {type(e).__name__}: {str(e)}")
        print("="*80 + "\n")
        state.subquestion_extractor_response = []
    
    return state


def column_name_extractor(state: TableExtractorState) -> str:
    print("\n" + "="*80)
    print("[TABLE EXTRACTOR - COLUMN] Starting column extraction")
    print("="*80)
    print(f"[TABLE EXTRACTOR - COLUMN] User Query: {state.user_query}")
    
    subquestions_resp = state.subquestion_extractor_response
    print(f"[TABLE EXTRACTOR - COLUMN] Subquestions to process: {len(subquestions_resp)}")
    
    # ✅ NEW: Validate if any subquestions exist
    if not subquestions_resp or subquestions_resp == [[]]:
        print(f"[TABLE EXTRACTOR - COLUMN] [WARNING] No valid subquestions to process")
        print(f"[TABLE EXTRACTOR - COLUMN] [WARNING] This may mean:")
        print(f"[TABLE EXTRACTOR - COLUMN]   • No relevant tables for the user query")
        print(f"[TABLE EXTRACTOR - COLUMN]   • Query is too generic or doesn't require filtering")
        print(f"[TABLE EXTRACTOR - COLUMN]   • Tables don't have metadata yet (run knowledgebaseAgent.py)")
        print(f"[TABLE EXTRACTOR - COLUMN] [SUCCESS] Column extraction completed (0 column set(s) extracted)")
        print("="*80 + "\n")
        state.selected_columns = []
        return state
    
    selected_columns = []
    
    for idx, subquestions in enumerate(subquestions_resp):
        # ✅ NEW: Validate subquestion structure
        if not subquestions or len(subquestions) < 2:
            print(f"[TABLE EXTRACTOR - COLUMN] [WARNING] Skipping invalid subquestion at index {idx}: {subquestions}")
            continue
        
        size = len(subquestions) - 1  # Last element is table name
        table_name = subquestions[size]
        
        # ✅ NEW: Validate table name
        if not table_name or not isinstance(table_name, str):
            print(f"[TABLE EXTRACTOR - COLUMN] [ERROR] Invalid table name in subquestion group {idx+1}: {table_name}")
            continue
        
        # ✅ NEW: Check if metadata exists for table
        if table_name not in knowledgebase_metadata:
            print(f"[TABLE EXTRACTOR - COLUMN] [WARNING] No metadata found for table '{table_name}'")
            print(f"[TABLE EXTRACTOR - COLUMN] [WARNING] Recommendation: Run knowledgebaseAgent.py to generate metadata for '{table_name}'")
            continue
        
        print(f"\n[TABLE EXTRACTOR - COLUMN] Processing subquestion group {idx+1}/{len(subquestions_resp)} (Table: {table_name})")
        
        for subq_idx in range(size):
            subquestion = subquestions[subq_idx]
            
            # ✅ NEW: Validate subquestion text
            if not subquestion or not isinstance(subquestion, str):
                print(f"[TABLE EXTRACTOR - COLUMN]   [WARNING] Skipping invalid subquestion at index {subq_idx}: {subquestion}")
                continue
            
            print(f"[TABLE EXTRACTOR - COLUMN]   |- Subquestion {subq_idx+1}/{size}: {subquestion}")
            
            try:
                table_metadata = knowledgebase_metadata.get(table_name, "")
                
                generate_columnExtractor_chain_res = generate_columnExtractor_chain.invoke({
                    "user_query": state.user_query,
                    "sub_question": subquestion,
                    "table_desc": table_metadata,
                    "agent_system_message": state.agent_system_message
                })
                print(f"[TABLE EXTRACTOR - COLUMN]   |  >> Extracted columns: {generate_columnExtractor_chain_res}")
                selected_columns.append(generate_columnExtractor_chain_res)
                
            except Exception as e:
                print(f"[TABLE EXTRACTOR - COLUMN]   |  >> [ERROR] Failed to extract columns: {type(e).__name__}: {str(e)}")
                print(f"[TABLE EXTRACTOR - COLUMN]   |  >> [INFO] Continuing with next subquestion...")
    
    state.selected_columns = selected_columns
    
    # ✅ NEW: Status message with details
    if selected_columns:
        print(f"\n[TABLE EXTRACTOR - COLUMN] [SUCCESS] Column extraction completed ({len(selected_columns)} column set(s) extracted)")
    else:
        print(f"\n[TABLE EXTRACTOR - COLUMN] [WARNING] No columns extracted from any subquestions")
        print(f"[TABLE EXTRACTOR - COLUMN] [INFO] This may be due to:")
        print(f"[TABLE EXTRACTOR - COLUMN]   • No valid subquestions were generated")
        print(f"[TABLE EXTRACTOR - COLUMN]   • Missing metadata for one or more tables")
        print(f"[TABLE EXTRACTOR - COLUMN]   • LLM unable to map subquestions to columns")
    
    print("="*80 + "\n")
    return state


table_extractor_graph_builder = StateGraph(TableExtractorState)
table_extractor_graph_builder.add_node(subquestion_extractor)
table_extractor_graph_builder.add_node(column_name_extractor)

table_extractor_graph_builder.add_edge(START,"subquestion_extractor")
table_extractor_graph_builder.add_edge("subquestion_extractor","column_name_extractor")
table_extractor_graph_builder.add_edge("column_name_extractor",END)
table_extractor_graph = table_extractor_graph_builder.compile()
