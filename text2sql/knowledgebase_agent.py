import time
from utils.db_utility import execute_query 
import pickle
import json
import os
from generate_table_metadata_chain import table_metadata_chain

def fetch_data(table):
    # Use RANDOM() for PostgreSQL instead of RAND() (which is MySQL syntax)

    query = 'SELECT * FROM {} ORDER BY RANDOM() LIMIT 10'.format(table)
    df_sample = execute_query(query)
    print(f"Table {table} has {df_sample}")
    return df_sample


def fetch_metadata():
    query = '''
    SELECT table_name FROM information_schema.tables WHERE table_schema = current_schema()
    AND table_type = 'BASE TABLE'
    '''
    table_list = execute_query(query)
    print(f"Fetched table list: {table_list}")
    return table_list


# ============================================================================
# KNOWLEDGE BASE GENERATION
# ============================================================================

print("\n" + "="*80)
print("STARTING KNOWLEDGEBASE METADATA EXTRACTION")
print("="*80 + "\n")


def populate_table_metadata():
    # Load existing metadata if temp file exists (for resume capability)
    metadata = {}
    if os.path.exists("knowledgebase_tmp_metadata.json"):
        try:
            with open("knowledgebase_tmp_metadata.json", 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            print(f"[KNOWLEDGEBASE] [INFO] Loaded {len(metadata)} tables from temp file")
        except Exception as e:
            print(f"[KNOWLEDGEBASE] [WARNING] Could not load temp file: {str(e)}")
            metadata = {}
    
    for table_name in fetch_metadata()['table_name'].tolist():
        print(f"[KNOWLEDGEBASE] Processing table: {table_name}")
        print("-" * 80)
        
        try:
            # Skip if already processed
            if table_name in metadata:
                print(f"[KNOWLEDGEBASE] [INFO] Table {table_name} already processed, skipping...")
                continue

            # Fetch sample data
            sample_df = fetch_data(table_name)
            sample_data_list = sample_df.to_dict(orient='records')
            
            print(f"[KNOWLEDGEBASE] [INFO] Fetched {len(sample_data_list)} sample records")
            
            # Invoke LLM to generate schema documentation
            print(f"[KNOWLEDGEBASE] [INFO] Generating schema documentation...")
            
            time.sleep(15)
            result = table_metadata_chain.invoke({
                "table_name": table_name,
                "sample_data": sample_data_list
            })
            
            metadata[table_name] = result
            
            print(f"[KNOWLEDGEBASE] [SUCCESS] Documentation generated for {table_name}")
            print(f"\nGenerated Documentation Preview:\n{result}...\n")
            
        except Exception as e:
            print(f"[KNOWLEDGEBASE] [ERROR] Failed to process {table_name}: {str(e)}")
            print(f"[KNOWLEDGEBASE] [ERROR] Skipping this table\n")
            #continue
    print(f"[KNOWLEDGEBASE] [INFO] Completed processing all tables.\n {metadata}")
    
    with open('knowledgebase_tmp_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)
        
    return metadata

from generate_domain_metadata_chain import domain_metadata_chain

def populate_domain_metadata(tables_metadata):
    time.sleep(5)
    domain_metadata = domain_metadata_chain.invoke({
        "tables_metadata": tables_metadata
    })
    print(f"[KNOWLEDGEBASE] [SUCCESS] Domain-level metadata generated {domain_metadata}")
    return domain_metadata

def save_metadata_to_file(domain_metadata):
    # Save metadata to file
    try:
        with open('knowledgebase_metadata.pkl', 'wb') as f:
            pickle.dump(domain_metadata, f)
        
        print("\n" + "="*80)
        print(f"[KNOWLEDGEBASE] [SUCCESS] Knowledge base saved to 'knowledgebase_metadata.pkl'")
        print(f"[KNOWLEDGEBASE] [INFO] Total tables processed: {len(domain_metadata)}")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"[KNOWLEDGEBASE] [ERROR] Failed to save metadata: {str(e)}\n")
        raise

def create_knowledgebase():
    table_metadata = populate_table_metadata()
    domain_metadata = populate_domain_metadata(table_metadata)
    save_metadata_to_file(domain_metadata)

create_knowledgebase();


