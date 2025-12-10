"""Query Generator Agent - Generates SQL query based on extracted information"""

import pickle

import chromadb
from agents.query_generator_agents.generate_query_chain import generate_sql_query_chain
from utils import chroma_db


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

        #Fetch RAG context
        rag_context_result = chroma_db.getRecords(user_query=state.user_query, domainId=1)
        
        # Handle empty RAG results - return empty string if no results
        if not rag_context_result or len(rag_context_result) == 0:
            rag_context = ""
            print(f"[AGENT] RAG context: No similar queries found")
        else:
            # Format RAG results into readable context
            rag_examples = []
            for idx, result in enumerate(rag_context_result, 1):
                relevance_score = result.get('relevance_score', 0)
                document = result.get('document', '')
                previous_generated_query = result.get('metadata', {}).get('generated_SQL', '')
                rag_examples.append(f"Example {idx} (Relevance: {relevance_score:.2f}):\n{document}\nPrevious Generated Query: {previous_generated_query}")

            rag_context = "\n\n".join(rag_examples)
            print(f"[AGENT] RAG context fetched: {len(rag_context_result)} record(s)")
        
        
        # Invoke SQL generation chain
        sql_query = generate_sql_query_chain.invoke({
            "user_query": state.user_query,
            "selected_columns": str(all_selected_columns),
            "filters": str(state.filters),
            "table_schema": table_schema,
            "rag_context": rag_context
        })
        
        state.generated_sql_query = sql_query
        print(f"[AGENT] [SUCCESS] SQL Query Generator completed\n")
        print(f"[AGENT] ================================================================================")
        print(f"[AGENT] FINAL GENERATED QUERY:")
        print(f"[AGENT] {state.generated_sql_query}")
        print(f"[AGENT] ================================================================================\n")
        
    except Exception as e:
        print(f"[AGENT] [ERROR] SQL Query Generator Error: {str(e)}\n")
        state.generated_sql_query = ""
    
    return state
