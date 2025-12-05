import chromadb
import uuid

# Initialize the Chroma client to connect to the running server
chroma_client = chromadb.HttpClient(host='localhost', port=8000)

# You can now interact with the database, e.g., check if it's alive:
print(chroma_client.heartbeat())

def createCollection():
    collection = chroma_client.create_collection(name="t2s_collection")
    return collection

def extractSQLMetadata(generated_SQL: str):
    pass

def addRecords(user_query: str, generated_SQL: str,domainId: int):
    if(chroma_client.get_collection(name="t2s_collection") is None):
        createCollection()
    
    collection = chroma_client.get_collection(name="t2s_collection")
    #sql_metadata = extractSQLMetadata(generated_SQL)
    # query_attributes = {   
    #                         "tables_used": sql_metadata["tables_used"],
    #                         "has_joins": sql_metadata["has_joins"],
    #                         "has_order_by": sql_metadata["has_order_by"],
    #                         "has_group_by": sql_metadata["has_group_by"],
    #                         "has_aggregations": sql_metadata["has_aggregations"]
    #                     }
    # enriched_documents = f"""
    #         User Query is : {user_query} and the 
    #         Generated SQL is : {generated_SQL} for the 
    #         domainId : {domainId}
    #         The generated query has following attributes {query_attributes}
    #         """
    enriched_documents = f"""
        User Query is : {user_query} and the 
        Generated SQL is : {generated_SQL} for the 
        domainId : {domainId}
        """
    collection.add(
        documents=[enriched_documents],
        metadatas=[{"domainId": domainId}],
        ids = [f"id_{domainId}_{uuid.uuid4()}"]
    )
    print(f"Record added to ChromaDB collection 't2s_collection' with domainId: {domainId}")

def getRecords(user_query: str, domainId: int):
    collection = chroma_client.get_collection(name="t2s_collection")
    results = collection.query(query_texts=[user_query], n_results=10, where={"domainId": domainId})
    relevant_results = fetch_relevant_records(results)
    return relevant_results

def fetch_relevant_records(results):
    """
    Filter relevant records by distance threshold
    Lower distance = higher relevance
    
    Distance threshold: 0.5 (cosine similarity)
    """
    relevant_result = []
    
    # Extract distances from results
    distances = results.get('distances', [[]])[0]
    documents = results.get('documents', [[]])[0]
    metadatas = results.get('metadatas', [[]])[0]
    
    # Filter by distance threshold (lower distance = more relevant)
    distance_threshold = 0.5  # Adjust based on your needs
    
    for distance, doc, metadata in zip(distances, documents, metadatas):
        if distance < distance_threshold:
            relevant_result.append({
                'document': doc,
                'metadata': metadata,
                'distance': distance,
                'relevance_score': 1 - distance  # Convert to relevance (0-1)
            })
    
    # Sort by distance (ascending - lower is better)
    relevant_result.sort(key=lambda x: x['distance'])
    
    return relevant_result