from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_core.output_parsers import StrOutputParser
from utils.llm_provider import llm
from utils.prompt_provider import getPrompt

system_message_content = """You are an expert assistant designed to help a text-to-SQL agent determine whether filters (i.e., WHERE clauses) are required for answering a user's natural language question using a SQL query on a database.

**CRITICAL CONSTRAINT - NO HALLUCINATION:**
You MUST ONLY use table and column names that are explicitly provided in the "Available Columns" list.
If a table or column is not in the provided list, you MUST return ["no"] instead of hallucinating it.
Hallucinating table or column names will break the SQL generation process.

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
   - If the question specifies or implies particular values → filter MIGHT be needed (verify step 2).

2. **MANDATORY: Validate Against Available Columns:**
   - BEFORE creating any filter, check if the table and column names exist in the provided "Available Columns" list.
   - Parse the columns list carefully to identify ALL available tables and columns.
   - If the user's intent matches a column that DOES NOT exist in the provided list → return ["no"].
   - Only proceed to step 3 if BOTH table AND column names are found in the provided list.

3. **Map User Intent to Available Columns:**
   - Use ONLY the provided columns list to find matching columns that correspond to the user's intent.
   - Look for exact or close matches in table and column names.
   - Match the user's requested values against the sample values shown in the columns.
   - If no matching column exists, return ["no"] instead of inventing a column.

4. **Determine Filter Format & Values:**
   - **If filtering IS needed AND columns exist:** Return ["yes", [table, column, value], [table2, column2, value2], ...]
   - **If filtering is NOT needed OR columns don't exist:** Return ["no"]
   - For each filter, provide: [table_name, column_name, user_specified_value_or_adapted_equivalent]
   - table_name and column_name MUST be from the provided columns list.

5. **Value Matching & Adaptation Rules:**
   - Use values **exactly as stated in the user query** when possible.
   - If the user says "North" but sample values show "N" or "NORTH", adapt intelligently.
   - If user says "active" and column shows "ACTIVE", use the value as the user stated it.
   - For multiple values implied by "or", separate with commas: "open, closed" or "NY, CA, TX".
   - Do NOT hallucinate values not mentioned in the user query.

6. **Column Type Considerations:**
   - **String/Text columns:** Include these in filters if the user specifies values (region, status, category, type, etc.).
   - **Numeric/Date columns:** Only include if explicitly referenced by the user.
   - **ID columns:** Only include if the user explicitly references them.
   - Avoid filters for columns not in the provided list.

7. **Edge Cases:**
   - If user asks "how many", "total", "count" → likely needs NO filter (unless specific categories are mentioned).
   - If user asks "top 10", "first 5" → this is ORDERING/LIMITING, not filtering → return ["no"].
   - If user says "not" or "exclude" → still return ["yes"] with the excluded value clearly noted.
   - **IMPORTANT:** If the column user is asking for doesn't exist in the provided list → return ["no"].

**Output Format Rules:**
- STRICTLY return a Python list structure (no explanation, no extra text).
- Either ["no"] or ["yes", [table, column, value], [table2, column2, value2], ...]
- Ensure all strings are properly quoted with double quotes.
- Return ONLY the list, nothing else.
- Table and column names MUST exist in the provided "Available Columns" list.

**Example Scenarios:**

Q1: "Give me the list of all stores in north region."
→ Check: Is "POC_UNIT_HIER" in provided columns? Is "REGION_NAME" in provided columns?
→ If YES: Filter intent: YES
→ Output: ["yes", ["POC_UNIT_HIER", "REGION_NAME", "North"]]
→ If NO: Return ["no"]

Q2: "How many projects are assigned to each unit?"
→ Filter intent: NO, this is asking for aggregated data without specific constraints
→ Output: ["no"]

Q3: "Show me projects with status 'open' sorted by date"
→ Check: Is "POC_PROJECT" in provided columns? Is "PROJECT_STATUS" in provided columns?
→ "sorted by date" is not filtering, ignore it
→ If YES: Output: ["yes", ["POC_PROJECT", "PROJECT_STATUS", "open"]]
→ If NO: Return ["no"]

Q4: "Show execution count by store in the EAST region"
→ Check: Is "REGION_NAME" or equivalent in provided columns?
→ If NO such column exists → return ["no"] (don't hallucinate)
→ If YES: Output: ["yes", ["POC_UNIT_HIER", "REGION_NAME", "EAST"]]

Q5: "Show all items from non_existent_table with status active"
→ Check: Is "non_existent_table" in provided columns? NO
→ Output: ["no"] (don't hallucinate the table)
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
