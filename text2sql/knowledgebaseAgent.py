import pandas as pd
from langchain_core.runnables import RunnableMap, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy import create_engine
from utils.llmProvider import llm
from utils.promptProvider import getPrompt
import pickle

# Manually Table Descriptions

tables_descriptions = {
    'POC_UNIT_HIER' : ''' It contain the data about the units/store hierarchy. This also have the unit information.''',
    'POC_PROJECT' : ''' It contains the data about the projects, including project. One Project is assigned to one or multiple units/stores.''',
    'POC_PROJECT_EXECUTION' : ''' It contains the data about the projects executions. When any project assigned to any unit. One instance is 
   #                               created of that for that unit, that one entry is stored in this table'''
}

# Fetching records from database
# db_connection = create_engine('db2+ibm_db://user:pass@localhost:50000/SAMPLE'); #  DB2 Example
# postgres example 
db_connection = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/postgres');
# db_connection = create_engine('sqlite:///sample.db'); # SQLite Example

def fetch_data(table):
    # Use RANDOM() for PostgreSQL instead of RAND() (which is MySQL syntax)
    query = 'SELECT * FROM {} ORDER BY RANDOM() LIMIT 10'.format(table)
    df_sample = pd.read_sql(query,db_connection)
    print(f"Table {table} has {df_sample}")
    return df_sample

# ============================================================================
# IMPROVED SYSTEM PROMPT - Database Schema Extractor
# ============================================================================
# Enhanced with:
# 1. Clearer instructions for data type identification
# 2. Examples of actual column patterns
# 3. Guidance on relationship detection
# 4. Better handling of NULL/missing values
# 5. Key constraints and data patterns

system_message_content = """You are an Expert Database Schema Knowledge Extractor Agent. Your mission is to analyze database table structures and sample data to create precise, actionable schema documentation for AI agents that will generate SQL queries.

**Your Goals:**
1. Extract structural information from the table schema
2. Infer data types, constraints, and patterns from sample records
3. Identify potential relationships (foreign keys, domain keys, hierarchy indicators)
4. Document valid value ranges and patterns
5. Note any anomalies or special characteristics

**Analysis Instructions:**

**Step 1: Table Analysis**
- Table Name: Extract exact name
- Purpose: Summarize the table's business function (what business data it captures)
- Row Count & Updates: Infer from data patterns (is it slowly changing? real-time? historical?)

**Step 2: Column Analysis** (For each column, determine):
- **Column Name:** Exact name as in database
- **Data Type:** Infer from sample values (integer, string, date, boolean, etc.)
- **Business Purpose:** What business concept does it represent?
- **Value Patterns:** What values are valid? Examples:
  - **Status/Flags:** Common values like 'active', 'inactive', 1, 0
  - **IDs/Keys:** Typically numeric, incremental, or formatted (e.g., PROJ-001)
  - **Dates:** Format patterns like YYYY-MM-DD
  - **Numeric Ranges:** Min/max values based on samples
- **Nullability:** Can it be NULL/missing?
- **Special Characteristics:** Is it a primary key? Foreign key? Hierarchy indicator?

**Step 3: Relationship Detection**
- Look for columns with "_ID", "_SKEY", "_KEY" suffixes → likely foreign keys
- Look for columns like "DOMAIN_ID" → multi-tenant isolation key
- Look for hierarchical patterns (parent_id, level_* columns)

**Step 4: Output Format**

---
**Table Name:** [Exact Table Name]

**Table Purpose:**
[1-2 sentences describing what business data this table stores]

**Characteristics:**
- **Data Nature:** [Real-time, historical, slowly-changing, transactional, etc.]
- **Primary Key:** [Column(s) that uniquely identify rows]
- **Key Relationships:** [Any detected foreign keys or relationships]

**Columns:**

*   **[Column Name 1]:**
    *   **Data Type:** [integer, varchar, date, boolean, etc.]
    *   **Purpose:** [What does this column represent?]
    *   **Sample Values:** [Examples from data]
    *   **Nullability:** [Can be NULL / Always populated]
    *   **Notes:** [Any special characteristics]

*   **[Column Name 2]:**
    *   **Data Type:** [type]
    *   **Purpose:** [Purpose]
    *   **Sample Values:** [Examples]
    *   **Nullability:** [Nullable / NOT NULL]
    *   **Notes:** [Special info]

---

**Real Example:**

---
**Table Name:** POC_PROJECT_EXECUTION

**Table Purpose:**
Tracks execution instances of projects assigned to organizational units. When a project is assigned to a unit, an execution record is created capturing status, timeline, and completion metrics for that assignment.

**Characteristics:**
- **Data Nature:** Transactional (updated as projects progress)
- **Primary Key:** EXEC_ID
- **Key Relationships:** Foreign key to POC_PROJECT (PROJECT_ID), Foreign key to POC_UNIT_HIER (UNIT_ID)

**Columns:**

*   **EXEC_ID:**
    *   **Data Type:** Integer
    *   **Purpose:** Unique identifier for each project execution instance
    *   **Sample Values:** 1, 2, 3, 101, 205
    *   **Nullability:** NOT NULL
    *   **Notes:** Primary Key, auto-incremented

*   **PROJECT_ID:**
    *   **Data Type:** Varchar/Text
    *   **Purpose:** References the project being executed
    *   **Sample Values:** PROJ-001, PROJ-002, PROJ-005
    *   **Nullability:** NOT NULL
    *   **Notes:** Foreign Key, formatted as PROJ-XXX

*   **UNIT_ID:**
    *   **Data Type:** Integer
    *   **Purpose:** The organizational unit to which the project is assigned
    *   **Sample Values:** 100, 101, 102, 103
    *   **Nullability:** NOT NULL
    *   **Notes:** Foreign Key, references POC_UNIT_HIER

*   **STATUS:**
    *   **Data Type:** Integer
    *   **Purpose:** Current execution status (lifecycle stage)
    *   **Sample Values:** 1, 2, 3, 4, 5, 6, 7 (likely representing stages: draft, active, pending, in-progress, on-hold, completed, cancelled)
    *   **Nullability:** NOT NULL
    *   **Notes:** Numeric status code, likely enum-like with 7 possible states

*   **START_DATE:**
    *   **Data Type:** Date/Timestamp
    *   **Purpose:** When the project execution started
    *   **Sample Values:** 2024-01-15, 2024-02-01
    *   **Nullability:** Can be NULL
    *   **Notes:** May be null if not yet started

---

**Apply this level of detail and structure to all provided tables.**
"""

human_message_content = """Analyze the following table and generate comprehensive schema documentation:

**Table Name:** {table_name}

**Table Description:** {table_description}

**Sample Data (10 records):**
{sample_data}

Generate detailed documentation following the format provided in system instructions. Focus on practical information that will help SQL generation agents understand available data and relationships."""

prompt = getPrompt(system_message_content, human_message_content)

task_one = RunnableLambda(lambda x: x["table_name"])
task_two = RunnableLambda(lambda x: x["table_description"])
task_three = RunnableLambda(lambda x: str(x["sample_data"]))  # Convert sample data to string for better LLM processing

final_task = RunnableMap({
    "table_name": task_one,
    "table_description": task_two,
    "sample_data": task_three,
})

# Creating LangChain
chain = final_task | prompt | llm | StrOutputParser()

# ============================================================================
# KNOWLEDGE BASE GENERATION
# ============================================================================

print("\n" + "="*80)
print("STARTING KNOWLEDGEBASE METADATA EXTRACTION")
print("="*80 + "\n")

metadata = {}

for table_name, table_description in tables_descriptions.items():
    print(f"[KNOWLEDGEBASE] Processing table: {table_name}")
    print("-" * 80)
    
    try:
        # Fetch sample data
        sample_df = fetch_data(table_name)
        sample_data_list = sample_df.to_dict(orient='records')
        
        print(f"[KNOWLEDGEBASE] [INFO] Fetched {len(sample_data_list)} sample records")
        
        # Invoke LLM to generate schema documentation
        print(f"[KNOWLEDGEBASE] [INFO] Generating schema documentation...")
        
        result = chain.invoke({
            "table_name": table_name,
            "table_description": table_description,
            "sample_data": sample_data_list
        })
        
        metadata[table_name] = result
        
        print(f"[KNOWLEDGEBASE] [SUCCESS] Documentation generated for {table_name}")
        print(f"\nGenerated Documentation Preview:\n{result[:200]}...\n")
        
    except Exception as e:
        print(f"[KNOWLEDGEBASE] [ERROR] Failed to process {table_name}: {str(e)}")
        print(f"[KNOWLEDGEBASE] [ERROR] Skipping this table\n")
        continue

# Save metadata to file
try:
    with open('knowledgebase_metadata.pkl', 'wb') as f:
        pickle.dump(metadata, f)
    
    print("\n" + "="*80)
    print(f"[KNOWLEDGEBASE] [SUCCESS] Knowledge base saved to 'knowledgebase_metadata.pkl'")
    print(f"[KNOWLEDGEBASE] [INFO] Total tables processed: {len(metadata)}")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"[KNOWLEDGEBASE] [ERROR] Failed to save metadata: {str(e)}\n")
    raise



