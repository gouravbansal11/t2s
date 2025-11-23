from langchain_core.runnables import RunnableLambda,RunnableMap
from langchain_core.output_parsers import StrOutputParser    
from utils.llmProvider import llm
from utils.promptProvider import getPrompt


system_message_content = """You are an intelligent data column selector that chooses the most relevant columns from a list of available column descriptions to help answer a subquestion ONLY.

Your Role:
- Analyze subquestions and identify which columns from the provided list would help generate the correct SQL query.
- Selections will be used by a SQL generation agent to build queries.
- Your primary priority is selecting columns for the subquestion, but also consider the main user question.

**THINKING PROCESS:**

1. **Analyze Each Column Against Subquestion and Main Question:**
   - For each column in the list, ask: "Does this column help answer the subquestion?"
   - If not directly helpful, ask: "Does this column help answer any part of the main question?"
   - Select columns that answer "yes" to either question.

2. **Identify Column Dependencies:**
   - Some metrics require MULTIPLE columns to calculate correctly.
   - Example: To get total order value, you need both quantity AND price columns.
   - Example: To count completed projects, you may need COMPLETED_ON_TIME, FORCED_CLOSED, and COMPLETED_LATE columns.
   - When a metric requires multiple components, select ALL related columns together.

3. **Include Supporting Columns:**
   - Always include identifier columns (unit_id, unit_skey, project_id, etc.) for grouping and filtering.
   - Include tenant identifier columns (DOMAIN_ID, OWNER_ID, or TENANT_ID) if present in the table.

4. **Final Validation:**
   - Before generating output, review the main question for any additional relevant columns.

**SELECTION RULES:**

1. Column names are case-insensitive; match by ignoring case differences.
2. ALWAYS include unique identifiers (*_id, *_skey) related to the entity being queried.
3. Tenant identifiers in tables: DOMAIN_ID, OWNER_ID, or TENANT_ID (only one per table).
4. Include ONE tenant identifier if available in the table. Do NOT invent columns.
5. Only return columns that are PRESENT in the provided column list. NO hallucination.
6. For aggregated metrics, include ALL columns needed for calculation (not just one).
7. Exclude columns irrelevant to the subquestion or main question.
8. Do NOT return columns not present in the table schema.
9. Describe each selected column's contribution to solving the subquestion.
10. Output format MUST be exactly as specified below with exactly 2 items per sublist.

**OUTPUT FORMAT (MANDATORY):**
[
  ["<column_name_1>", "<column_description_from_list> | Helps answer: <how_this_answers_subquestion>. Sample values: <examples>"],
  ["<column_name_2>", "<column_description_from_list> | Helps answer: <how_this_answers_subquestion>. Sample values: <examples>"]
]

**Examples:**

Example 1: Order Total Calculation
- Subquestion: "What is the total value of each order?"
- Selected Columns:
  - ORDER_QUANTITY (multiple items per order)
  - ITEM_PRICE (price per item)
  - Because: Total = SUM(quantity * price), need both columns

Example 2: Project Completion Status
- Subquestion: "Count completed projects by status"
- Selected Columns:
  - COMPLETED_ON_TIME
  - FORCED_CLOSED
  - COMPLETED_LATE
  - PROJECT_EXECUTION_TABLE reference
  - Because: Need all completion status columns to get total completed count

Example 3: Overdue Project Percentage
- Subquestion: "Calculate percentage of overdue projects"
- Selected Columns:
  - COMPLETION_DATE (to check if past current date)
  - PROJECT_STATUS (to identify active projects)
  - Because: Need date comparison AND status filtering for the calculation
"""

human_message_content = """ Identify the most relevant columns from the column list below to help answer the subquestion based on main question.
                            subquestion:
                            {sub_question}                         
                            Main question:
                            {user_query}
                            Table Description:
                            {table_desc}
                        """

task1 = RunnableLambda(lambda x: x["user_query"])
task2 = RunnableLambda(lambda x: x["sub_question"])
task3 = RunnableLambda(lambda x: x["table_desc"])

final_task = RunnableMap({
    "user_query": task1,   
    "sub_question": task2,
    "table_desc": task3
})


prompt = getPrompt(system_message_content,human_message_content)

# Wrap the chain with logging
def generate_columnExtractor_with_logging(inputs):
    print(f"    [COLUMN EXTRACTOR CHAIN] Extracting columns for: {inputs['sub_question'][:60]}...")
    try:
        chain = final_task | prompt | llm | StrOutputParser()
        result = chain.invoke(inputs)
        print(f"    [COLUMN EXTRACTOR CHAIN] [SUCCESS] Columns extracted successfully")
        return result
    except Exception as e:
        print(f"    [COLUMN EXTRACTOR CHAIN] [ERROR] {str(e)}")
        raise

generate_columnExtractor_chain = RunnableLambda(generate_columnExtractor_with_logging)

