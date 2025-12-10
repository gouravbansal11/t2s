import chromadb
import uuid

# Initialize the Chroma client to connect to the running server
chroma_client = chromadb.HttpClient(host='localhost', port=8000)

# You can now interact with the database, e.g., check if it's alive:
print(chroma_client.heartbeat())

def createCollection():
    collection = chroma_client.create_collection(name="t2s_collection")
    return collection

def isCollectionExists():
    try:
        collection = chroma_client.get_collection(name="t2s_collection")
        return True
    except Exception as e:
        print(f"Error checking collection existence: {str(e)}")
        return False
    except chromadb.errors.NotFoundError as e:
        print(f"Collection not found: {str(e)}")    
        return False

def extractSQLMetadata(generated_SQL: str):
    pass

def addRecords(user_query: str, generated_SQL: str,domainId: int):
    if(isCollectionExists() == False):
        print("Collection does not exist")
        createCollection()

    print("Adding RAG data to Collection")
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
    # enriched_documents = f"""
    #     User Query is : {user_query} and the 
    #     Generated SQL is : {generated_SQL} for the 
    #     domainId : {domainId}
    #     """
    #
    enriched_documents = f"""
        User Query is : {user_query}
        """
    collection.add(
        documents=[enriched_documents],
        metadatas=[{"domainId": domainId, "generated_SQL": generated_SQL}],
        ids = [f"id_{domainId}_{uuid.uuid4()}"]
    )
    print(f"Record added to ChromaDB collection 't2s_collection' with domainId: {domainId}")

def getRecords(user_query: str, domainId: int):
    try:
        collection = chroma_client.get_collection(name="t2s_collection")
        results = collection.query(query_texts=[user_query], n_results=10, where={"domainId": domainId})
        print(f"ChromaDB query results: {results}")
        relevant_results = fetch_relevant_records(results)
        return relevant_results
    except Exception as e:
        print(f"Error fetching records from ChromaDB: {str(e)}")
        return []

def fetch_relevant_records(results):
    """
    Filter relevant records by distance threshold
    Lower distance = higher relevance
    
    ChromaDB COSINE DISTANCE SCALE:
    - 0.0 = Perfect match (identical)
    - 0.5 = Very similar
    - 1.0 = Moderately similar
    - 1.5 = Somewhat similar
    - 2.0 = Completely different
    
    Distance threshold: 1.5 (accepts moderately similar queries)
    """
    relevant_result = []
    
    # Extract distances from results
    distances = results.get('distances', [[]])[0]
    documents = results.get('documents', [[]])[0]
    metadatas = results.get('metadatas', [[]])[0]
    
    # Filter by distance threshold (lower distance = more relevant)
    # Adjusted from 0.5 to 1.1 to capture moderately similar queries
    distance_threshold = 1
    
    for distance, doc, metadata in zip(distances, documents, metadatas):
        if distance < distance_threshold:
            relevant_result.append({
                'document': doc,
                'metadata': metadata,
                'distance': distance,
                'relevance_score': 1 - (distance / 2)  # Normalize to 0-1 range
            })
    
    print(f"Relevant records found: {relevant_result}")
    # Sort by distance (ascending - lower is better)
    relevant_result.sort(key=lambda x: x['distance'])
    
    print(f"Found the following relevant records:\n\n {relevant_result} \n\n")
    return relevant_result