from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_core.output_parsers import StrOutputParser
from utils.llmProvider import llm
from utils.promptProvider import getPrompt

system_message_content = """You are an expert assistant designed to help a text-to-SQL agent determine whether filters (i.e., WHERE clauses) are required for answering a user's natural language question using a SQL query on a database.

**Your Primary Task:**
Analyze the user's natural language question and determine if any WHERE clause conditions are needed. A filter is needed when the user is asking for:
- Specific values (e.g., "stores in North region", "projects with status 'open'")
- Categorical selections (e.g., "payment method is credit card", "region is California")
- Specific date ranges or points in time (if date columns are available)
- Exclusions or inclusions of specific categories

**Step-by-Step Analysis:**

1. **Identify Filtering Intent:**
   - Read the user question carefully to understand what specific values or categories they're asking for.
   - Look for keywords: "where", "in", "is", "equals", "like", "between", "from", "to", "region", "status", "category", "type", etc.
   - If the question asks for "all", "list", "count", "total" without specific constraints → likely NO filter needed.
   - If the question specifies or implies particular values → filter IS needed.

2. **Map User Intent to Available Columns:**
   - Use the provided columns list to find matching columns that correspond to the user's intent.
   - Look for columns with names/descriptions containing: status, region, type, category, state, district, domain, etc.
   - Match the user's requested values against the sample values shown in the columns (adapt case/format as needed).

3. **Determine Filter Format & Values:**
   - **If filtering IS needed:** Return ["yes", [table, column, value], [table2, column2, value2], ...]
   - **If filtering is NOT needed:** Return ["no"]
   - For each filter, provide: [table_name, column_name, user_specified_value_or_adapted_equivalent]

4. **Value Matching & Adaptation Rules:**
   - Use values **exactly as stated in the user query** when possible.
   - If the user says "North" but sample values show "N" or "NORTH", adapt intelligently (use "North" as primary, but note abbreviations).
   - If user says "active" and column shows "ACTIVE", use the value as the user stated it.
   - For multiple values implied by "or", separate with commas: "open, closed" or "NY, CA, TX".
   - Do NOT hallucinate values not mentioned in the user query.

5. **Column Type Considerations:**
   - **String/Text columns:** Include these in filters if the user specifies values (region, status, category, type, etc.).
   - **Numeric/Date columns:** Only include if explicitly referenced by the user (e.g., "greater than 100", "after 2025-01-01").
   - **ID columns:** Only include if the user explicitly references them (e.g., "project ID 123").
   - Avoid filters for purely aggregation keys unless explicitly requested.

6. **Edge Cases:**
   - If user asks "how many", "total", "count" → likely needs NO filter (unless specific categories are mentioned).
   - If user asks "top 10", "first 5" → this is ORDERING/LIMITING, not filtering → return ["no"].
   - If user says "not" or "exclude" → still return ["yes"] with the excluded value clearly noted.

**Output Format Rules:**
- STRICTLY return a Python list structure (no explanation, no extra text).
- Either ["no"] or ["yes", [table, column, value], [table2, column2, value2], ...]
- Ensure all strings are properly quoted with double quotes.
- Return ONLY the list, nothing else.

**Example Scenarios:**

Q1: "Give me the list of all stores in north region."
→ Filter intent: YES, user wants stores in "north" region
→ Output: ["yes", ["POC_UNIT_HIER", "REGION_NAME", "North"]]

Q2: "How many projects are assigned to each unit?"
→ Filter intent: NO, this is asking for aggregated data without specific constraints
→ Output: ["no"]

Q3: "Show me projects with status 'open' or 'in progress' in the California region"
→ Filter intent: YES, multiple conditions
→ Output: ["yes", ["POC_PROJECT", "PROJECT_STATUS", "open, in progress"], ["POC_UNIT_HIER", "REGION_NAME", "California"]]

Q4: "List the top 5 most executed projects"
→ Filter intent: NO, this is asking for sorted/limited results, not filtering by specific values
→ Output: ["no"]

Q5: "Show all project executions that are overdue or pending"
→ Filter intent: YES, user specifies status values
→ Output: ["yes", ["POC_PROJECT_EXECUTION", "EXECUTION_STATUS", "overdue, pending"]]
"""

human_message_content = """Analyze the user's question and determine if SQL WHERE clauses are needed.

**User Question:**
{user_query}

**Available Columns (with table and description context):**
{columns}

**Your Task:**
1. Determine if the user is asking for specific filtered values or all data.
2. If filtering is needed, identify which columns from the available list would be used.
3. Return your answer in STRICTLY list format:
   - ["no"] if no filters are needed
   - ["yes", [table, column, value], ...] if filters are needed

**Important:** Return ONLY the list structure, no explanations or additional text.
"""

task1 = RunnableLambda(lambda x: x["user_query"])
task2 = RunnableLambda(lambda x: x["columns"])

final_task = RunnableMap({
    "user_query": task1,   
    "columns": task2
})

prompt = getPrompt(system_message_content, human_message_content)

# Wrap the chain with logging
def filter_check_with_logging(inputs):
    print("\n" + "="*80)
    print("[FILTER CHECK AGENT] Starting filter detection")
    print("="*80)
    print(f"[FILTER CHECK AGENT] User Query: {inputs['user_query']}")
    print(f"[FILTER CHECK AGENT] Available Columns: {inputs['columns']}")
    
    try:
        # Invoke the chain
        chain = final_task | prompt | llm | StrOutputParser()
        result = chain.invoke(inputs)
        print(f"[FILTER CHECK AGENT] Filter Analysis Result: {result}")
        print(f"[FILTER CHECK AGENT] [SUCCESS] Filter detection completed successfully")
        print("="*80 + "\n")
        return result
    except Exception as e:
        print(f"[FILTER CHECK AGENT] [ERROR] Error during filter check: {str(e)}")
        print("="*80 + "\n")
        raise

check_filter_agent_chain = RunnableLambda(filter_check_with_logging)
