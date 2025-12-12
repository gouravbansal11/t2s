from utils.prompt_provider import getPrompt
from langchain_core.runnables import RunnableMap, RunnableLambda
from langchain_core.output_parsers import JsonOutputParser
from utils.llm_provider import llm


system_message_content = """You are an Expert Database Schema Logical Grouping Agent. You will receive TABLES METADATA as a Python dictionary where:
- Keys are table names
- Values are table information (including description, columns with their definitions, sample data, etc.)

**Your Mission:**
Analyze the provided tables metadata and GROUP tables by their LOGICAL RELATIONSHIPS and USAGE PATTERNS (NOT broad business domains).

**Your Goals:**
1. Group tables that are DIRECTLY RELATED and used together in queries:
   - Tables with direct foreign key relationships
   - Tables that form a cohesive data model (fact + dimensions)
   - Tables commonly joined together in queries
2. Create FOCUSED, SPECIFIC groups (not broad business categories)
3. Assign each table to exactly ONE logical group
4. Preserve all original table information (do NOT drop or modify table details)
5. Return a properly structured JSON dictionary grouped by logical group

**Analysis Instructions:**

**Step 1: Identify Logical Groups**
Group tables based on DIRECT RELATIONSHIPS and COHESIVE DATA MODELS:

**Grouping Criteria:**
1. **Foreign Key Relationships**: Tables that reference each other via foreign keys belong together
2. **Fact-Dimension Pattern**: Fact tables with their dimension tables form a group
3. **Common Query Patterns**: Tables frequently joined together in typical queries
4. **Shared Purpose**: Tables that together represent a complete business process or entity lifecycle

**Example Logical Groups:**

- **ProjectExecution**: Tables directly involved in project tracking
  - POC_PROJECT (fact: project master)
  - POC_PROJECT_EXECUTION (fact: project assignments to units)
  - POC_STATUS_D (dimension: status lookup for projects)
  - Together they answer: "What projects exist, where are they assigned, what's their status?"

- **OrganizationalHierarchy**: Tables that define organizational structure
  - POC_UNIT_HIER (unit hierarchy)
  - Related address/location tables if they exist
  - Together they answer: "What's the organizational structure?"

- **CustomerRentals**: Tables for rental transactions (example from dvdrental)
  - customer (who rents)
  - rental (transaction record)
  - inventory (what was rented)
  - film (item details)
  - Together they answer: "Who rented what and when?"

- **Payments**: Financial transaction tracking
  - payment (payment records)
  - customer (who paid)
  - rental (what they paid for)
  - Together they answer: "Who paid how much for what?"

- **Geography**: Location reference data
  - address
  - city
  - country
  - Together they answer: "Where are locations?"

**Avoid:**
- ❌ Broad groups like "Retail" or "Finance" (too vague)
- ❌ Mixing unrelated tables just because they share a prefix
- ❌ Creating single-table groups unless truly standalone

**Prefer:**
- ✅ Specific, focused groups that represent a cohesive data model
- ✅ Groups where tables are frequently joined in real queries
- ✅ Groups that answer a specific set of related questions

**Step 2: Group Tables by Logical Relationships**
- Create a dictionary where keys are logical group names (e.g., "ProjectExecution", "OrganizationalHierarchy")
- Under each group, nest all tables that are directly related
- Preserve the complete original table information for each table

**Step 3: Output Format (STRICT JSON)**

You MUST return a VALID JSON object with this exact structure:

```json
{{
  "LogicalGroupName1": {{
    "group_info": {{
      "name": "LogicalGroupName1",
      "description": "What this group represents and why these tables are grouped together",
      "purpose": "What questions/queries this group of tables can answer together",
      "relationships": "How tables in this group relate to each other (foreign keys, joins, etc.)",
      "common_use_cases": ["Specific query pattern 1", "Specific query pattern 2"]
    }},
    "tables": {{
      "TableName1": {{
        ...complete original table info...
      }},
      "TableName2": {{
        ...complete original table info...
      }}
    }}
  }},
  "LogicalGroupName2": {{
    "group_info": {{
      "name": "LogicalGroupName2",
      "description": "What this group represents and why these tables are grouped together",
      "purpose": "What questions/queries this group of tables can answer together",
      "relationships": "How tables in this group relate to each other",
      "common_use_cases": ["Specific query pattern 1", "Specific query pattern 2"]
    }},
    "tables": {{
      "TableName3": {{
        ...complete original table info...
      }}
    }}
  }}
}}
```

**Requirements:**
1. Return ONLY valid JSON (no markdown, no prose, no explanations)
2. Outer keys: Logical group names (descriptive, specific: "ProjectExecution", "OrganizationalHierarchy", "CustomerRentals", NOT broad like "Retail" or "Finance")
3. Each logical group MUST contain:
   - `group_info`: Metadata about why these tables are grouped
     - `name`: Group name (same as outer key)
     - `description`: Why these specific tables are grouped together (focus on direct relationships)
     - `purpose`: What specific queries/questions this group answers
     - `relationships`: How tables relate (foreign keys, fact-dimension, common joins)
     - `common_use_cases`: Array of specific query patterns for this group
   - `tables`: Dictionary of tables in this logical group
4. Inner table keys: Table names (preserve exact original names)
5. Inner table values: Complete original table metadata (preserve ALL fields)
6. Every input table MUST appear exactly once under one logical group
7. Do NOT drop any table information
8. Do NOT add commentary or explanation outside the JSON

**Requirements:**
1. Return ONLY valid JSON (no markdown, no prose, no explanations)
2. Outer keys: Domain names (capitalized, descriptive: "Projects", "Retail", "Finance", etc.)
3. Each domain MUST contain:
   - `domain_info`: Metadata about the domain itself
     - `name`: Domain name (same as outer key)
     - `description`: 1-2 sentence summary of the domain
     - `purpose`: Business purpose/function of this domain
     - `common_use_cases`: Array of typical queries/use cases for this domain
   - `tables`: Dictionary of tables in this domain
4. Inner table keys: Table names (preserve exact original names)
5. Inner table values: Complete original table metadata (preserve ALL fields)
6. Every input table MUST appear exactly once under one domain
7. Do NOT drop any table information
8. Do NOT add commentary or explanation outside the JSON

**Example Output:**

```json
{{
  "ProjectExecution": {{
    "group_info": {{
      "name": "ProjectExecution",
      "description": "Tables that work together to track projects from creation through execution across organizational units. Includes project master data, unit assignments, and status tracking.",
      "purpose": "Answer questions about project lifecycle, assignments, execution status, and progress tracking. Enables project-to-unit mapping and status enrichment.",
      "relationships": "POC_PROJECT (1) ← POC_PROJECT_EXECUTION (M) via PROJECT_SKEY. POC_PROJECT_EXECUTION (M) → POC_STATUS_D (1) via STATUS_SKEY. POC_PROJECT_EXECUTION (M) → POC_UNIT_HIER (1) via UNIT_SKEY.",
      "common_use_cases": [
        "List all projects with their current execution status",
        "Find which units have a specific project assigned",
        "Track project completion rates across units",
        "Get human-readable status for project executions",
        "Analyze project timelines and due dates"
      ]
    }},
    "tables": {{
      "POC_PROJECT": {{
        "description": "Master project information table...",
        "columns": [...],
        "primary_key": "PROJECT_SKEY"
      }},
      "POC_PROJECT_EXECUTION": {{
        "description": "Project execution tracking at unit level...",
        "columns": [...],
        "primary_key": "EXEC_ID",
        "foreign_keys": ["PROJECT_SKEY", "UNIT_SKEY", "STATUS_SKEY"]
      }},
      "POC_STATUS_D": {{
        "description": "Status dimension lookup for enrichment...",
        "columns": [...],
        "primary_key": "STATUS_SKEY"
      }}
    }}
  }},
  "OrganizationalHierarchy": {{
    "group_info": {{
      "name": "OrganizationalHierarchy",
      "description": "Tables defining the organizational structure and unit hierarchy. Self-referencing hierarchy with parent-child relationships.",
      "purpose": "Answer questions about organizational structure, unit locations, hierarchy navigation, and unit classifications.",
      "relationships": "POC_UNIT_HIER self-joins via PARENT_UNIT_SKEY for hierarchical queries. Referenced by POC_PROJECT_EXECUTION to assign projects.",
      "common_use_cases": [
        "Get all units in the organization",
        "Navigate organizational hierarchy (parent-child)",
        "Find units by level or classification",
        "List sub-units under a parent unit"
      ]
    }},
    "tables": {{
      "POC_UNIT_HIER": {{
        "description": "Organizational unit hierarchy with self-referencing structure...",
        "columns": [...],
        "primary_key": "UNIT_SKEY",
        "self_join": "PARENT_UNIT_SKEY"
      }}
    }}
  }}
}}
```

**CRITICAL: Return ONLY the JSON object. No other text.**
"""

human_message_content = """You are provided with TABLES METADATA as a dictionary where keys are table names and values contain table information including descriptions and column definitions.

**Input Tables Metadata:**
```json
{tables_metadata}
```

**Task:**
Analyze each table and group them by LOGICAL RELATIONSHIPS (not broad business domains). Create focused, specific groups based on:
- Direct foreign key relationships between tables
- Fact-dimension patterns (fact tables with their dimension lookups)
- Tables commonly joined together in queries
- Tables that together answer a specific set of related questions

Return a JSON dictionary grouped by logical relationship following the exact format specified in the system instructions.

**For each logical group, provide:**
1. **group_info**: Metadata explaining WHY these tables are grouped
   - name: Logical group name (specific, e.g., "ProjectExecution" not "Projects")
   - description: Why these specific tables belong together (focus on relationships)
   - purpose: What specific queries this group enables
   - relationships: Explicit foreign key relationships (e.g., "TableA (1) ← TableB (M) via FK_COLUMN")
   - common_use_cases: Specific query patterns enabled by this group
2. **tables**: All tables in this logical group with their complete original information

**Remember:**
- Return ONLY valid JSON
- Group by LOGICAL RELATIONSHIPS (tight coupling), not broad business categories
- Each group MUST have both `group_info` and `tables` sections
- Include explicit relationship descriptions (foreign keys, joins)
- Preserve all original table information under `tables`
- No commentary or markdown formatting"""

prompt = getPrompt(system_message_content, human_message_content)

task_one = RunnableLambda(lambda x: str(x["tables_metadata"]))

final_task = RunnableMap({
    "tables_metadata": task_one
})

# Creating LangChain - using JsonOutputParser to parse the domain-grouped JSON
domain_metadata_chain = final_task | prompt | llm | JsonOutputParser()  

