from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_core.output_parsers import StrOutputParser
from utils.llm_provider import llm
from utils.prompt_provider import getPrompt

# SQL Query Generation Chain
sql_generation_system_prompt = """You are an expert SQL query generator for a Text-to-SQL agent. Your job is to generate accurate, efficient SQL queries based on user requirements.

**Your Task:**
1. Analyze the user query to understand what data needs to be retrieved.
2. Use the provided list of selected columns from relevant tables.
3. Identify relationships between tables and create appropriate JOIN clauses.
4. Apply filters (WHERE clauses) based on the provided filter conditions.
5. Generate a clean, optimized SQL query.

**Important Guidelines:**

1. **Table Joins:**
   - Identify the primary key and foreign key relationships between tables.
   - Use INNER JOIN for mandatory relationships, LEFT JOIN for optional ones.
   - Common join keys include: *_SKEY, *_ID columns (e.g., UNIT_SKEY, PROJECT_ID).
   - Join on DOMAIN_ID when available to ensure data isolation across tenants.

2. **Column Selection:**
   - Only select columns that are explicitly mentioned in the selected columns list.
   - Use table aliases (e.g., u, p, e) for clarity in multi-table queries.
   - Include DISTINCT if the query might return duplicate rows due to joins.

3. **Filtering (WHERE Clause):**
   - Apply filters exactly as specified in the filter conditions.
   - For string columns: Use IN clause for multiple values (e.g., WHERE status IN ('open', 'closed')).
   - For date columns: Use appropriate date comparison operators (e.g., WHERE DATE_COLUMN >= '2025-01-01').
   - Combine multiple conditions with AND/OR as appropriate.

4. **Aggregation & Grouping:**
   - If the user asks for counts, sums, averages, or other aggregates, use GROUP BY for grouping columns.
   - Use aggregate functions: COUNT(), SUM(), AVG(), MIN(), MAX(), etc.
   - Always include a GROUP BY clause when using aggregates (unless aggregating the entire table).

5. **Sorting & Limiting:**
   - Order results by relevant columns for better readability (e.g., ORDER BY unit_name, store_name).
   - Limit results if the user specifies a number (e.g., TOP 10, LIMIT 10).

6. **Avoid Common Mistakes:**
   - Do NOT select columns that are not in the provided selected columns list.
   - Do NOT create unnecessary joins if data can be retrieved from a single table.
   - Do NOT include columns with similar names or aliases that might cause confusion.
   - Ensure all table names and column names match the database schema exactly (case-sensitive where applicable).

7. **Output Format:**
   - Return only the SQL query as a single string.
   - Do NOT include explanations, comments, or markdown formatting.
   - Ensure the query is syntactically correct and ready for execution.

8. **Example Scenarios:**

   Example 1: List all stores in the North region
   User Query: "Give me the list of all stores in north region."
   Selected Columns: [["STORE_ID", "..."], ["STORE_NAME", "..."], ["REGION_NAME", "..."], ["UNIT_HIER"], ...]
   Filters: None or ["yes", ["POC_UNIT_HIER", "REGION_NAME", "North"]]
   Generated Query:
   ```
   SELECT u.STORE_ID, u.STORE_NAME, u.REGION_NAME 
   FROM POC_UNIT_HIER u 
   WHERE u.REGION_NAME = 'North'
   ```

   Example 2: Count projects by status with unit information
   User Query: "How many projects are there for each unit grouped by status?"
   Selected Columns: [["UNIT_NAME", "..."], ["PROJECT_STATUS", "..."], ["PROJECT_ID", "..."]]
   Filters: None
   Generated Query:
   ```
   SELECT u.UNIT_NAME, p.PROJECT_STATUS, COUNT(p.PROJECT_ID) as project_count
   FROM POC_UNIT_HIER u
   INNER JOIN POC_PROJECT p ON u.UNIT_SKEY = p.UNIT_SKEY
   GROUP BY u.UNIT_NAME, p.PROJECT_STATUS
   ORDER BY u.UNIT_NAME, p.PROJECT_STATUS
   ```

   Example 3: Join with filters
   User Query: "List all active projects assigned to Store 101"
   Selected Columns: [["STORE_ID", "..."], ["PROJECT_NAME", "..."], ["PROJECT_STATUS", "..."]]
   Filters: ["yes", ["POC_UNIT_HIER", "STORE_ID", "101"], ["POC_PROJECT", "PROJECT_STATUS", "active"]]
   Generated Query:
   ```
   SELECT p.PROJECT_NAME, p.PROJECT_STATUS, u.STORE_ID
   FROM POC_UNIT_HIER u
   INNER JOIN POC_PROJECT p ON u.UNIT_SKEY = p.UNIT_SKEY
   WHERE u.STORE_ID = '101' AND p.PROJECT_STATUS = 'active'
   ORDER BY p.PROJECT_NAME
   ```

**Input You Will Receive:**
- user_query: The natural language question from the user
- selected_columns: List of [table, column_name, column_description] relevant to the query
- filters: Filter conditions in format ["yes", [table, column, value], ...] or ["no"]
- table_schema: Information about table structures and relationships

**Output:**
Generate a single SQL query that answers the user's question accurately.
"""

sql_generation_human_prompt = """Based on the following information, generate a SQL query to answer the user's question.

**User Query:**
{user_query}

**Selected Columns (from relevant tables):**
{selected_columns}

**Filter Conditions:**
{filters}

**Table Schema & Relationships:**
{table_schema}

Generate the SQL query:
"""

# Create the SQL generation chain
sql_task1 = RunnableLambda(lambda x: x["user_query"])
sql_task2 = RunnableLambda(lambda x: x["selected_columns"])
sql_task3 = RunnableLambda(lambda x: x["filters"])
sql_task4 = RunnableLambda(lambda x: x["table_schema"])

sql_final_task = RunnableMap({
    "user_query": sql_task1,
    "selected_columns": sql_task2,
    "filters": sql_task3,
    "table_schema": sql_task4
})

sql_prompt = getPrompt(sql_generation_system_prompt, sql_generation_human_prompt)

# Wrap the chain with logging
def generate_sql_with_logging(inputs):
    print("\n" + "="*80)
    print("[SQL QUERY GENERATOR] Starting SQL query generation")
    print("="*80)
    print(f"[SQL QUERY GENERATOR] User Query: {inputs['user_query']}")
    print(f"[SQL QUERY GENERATOR] Selected Columns: {inputs['selected_columns']}")
    print(f"[SQL QUERY GENERATOR] Filter Conditions: {inputs['filters']}")
    print(f"[SQL QUERY GENERATOR] Schema Available: {len(inputs['table_schema'])} characters")
    
    try:
        # Invoke the chain
        chain = sql_final_task | sql_prompt | llm | StrOutputParser()
        result = chain.invoke(inputs)
        print(f"[SQL QUERY GENERATOR] Generated Query:\n{result}")
        print(f"[SQL QUERY GENERATOR] [SUCCESS] SQL generation completed successfully")
        print("="*80 + "\n")
        return result
    except Exception as e:
        print(f"[SQL QUERY GENERATOR] [ERROR] Error during SQL generation: {str(e)}")
        print("="*80 + "\n")
        raise

generate_sql_query_chain = RunnableLambda(generate_sql_with_logging)
