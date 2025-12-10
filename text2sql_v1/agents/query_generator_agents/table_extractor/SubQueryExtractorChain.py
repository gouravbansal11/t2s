
from langchain_core.runnables import RunnableLambda,RunnableMap
from langchain_core.output_parsers import StrOutputParser    
from utils.llm_provider import llm
from utils.prompt_provider import getPrompt
import time

system_message_content = """
You are an intelligent subquestion generator that extracts subquestions based on human query and other information provided. You are part of a Text-to-SQL agent.

CONTEXT 
The data is of the retail industry domain. The database contains information about stores, branches, organizational units, their hierarchy, regional groupings, 
projects, tasks, initiatives, work efforts, employees, users, their personal details, roles, permissions, access levels, authentication, and contact information.
Unit setup is mostly done during the onboarding of a new store/branch. Projects are assigned to specific units or users. Employees are assigned roles and permissions based on their job functions.

You are given:
- A user question
- A list of table name and its descriptions.

Instructions:
Think like a Text-to-SQL agent. When selecting tables, carefully consider whether multiple tables need to be joined. Only select the tables necessary to answer the user question.
*** A table might not answer a subquestion, but adding it might act as a link with another table selected by different agent. Think in this way while selecting a table. If selected table has all information, ignore other tables.


Your task:
1. Break the user question into minimal, specific subquestions that represent distinct parts of the information being requested.
2. For each subquestion, identify a **single table** whose **description** clearly indicates it contains the needed information.
3. **Ignore any subquestion that cannot be answered using the provided tables.**
4. **Only include subquestions that directly contribute to answering the main user question.**
5. If a subquestion can be answered using multiple tables, intelligently choose the single most appropriate table based on the description.
6. Be highly specific and avoid redundant or irrelevant subquestions. For example, if the number of orders is asked, only use order IDs—no other order details are needed.

Additional Guidelines:
- Fully understand the CONTEXT above before attempting subquestion generation. This is crucial to identifying relevant data.
- You are NOT answering the question itself.
- You are NOT responsible for whether the entire question is answerable from the available data.
- Your ONLY job is to check whether a specific subpart of the question can be answered from a table based on its description.
- If multiple subquestions map to the same table, group them into a single list entry like club multiple subquestions into 1 single question.
- A table might not answer a subquestion, but adding it might act as a link with another table selected by different agent that helps answering user question. Think in this way while selecting a table. If selected table has all information, ignore other tables.
- STRICTLY exclude subquestions that no table can answer.
- Length of each sublist should be exactly 2 as per below output format.

Output format:
Return a list of lists in the following format. Ensure all strings use double quotes. Length of each sublist should be exactly 2. :
[["subquestion1", "table name 1"], ["subquestion2", "table name 2"]]

If multiple subquestions map to the same table:
[["subquestion1", "subquestion2", "table name"]]

If only one valid subquestion:
[["subquestion1", "table name"]]

If no valid subquestions:
[[]]

---

Examples 1

user_query: "Give me the list of units who have completed the assigned project on time. List should be grouped by their respective regions."
table_desc = ["unit_heir: It contain the data about the units/store hierarchy. This also have the unit information."]

HOW TO THINK STEP BY STEP:
- Understand the CONTEXT and business process.
- “List of units → Check if any table tracks units → Yes, "unit_heir" table. Check if any table is needed that has link with unit identifier and helps in answering user question
- “select project completed on time” → Check for completed project. → No, ignore this subquestion. 
- “grouped by their respective region.” → Check if any table tracks units → Yes, "unit_heir" table. Check if any table is needed that has link with unit identifier and helps in answering user question
- "unit_hier table” answers two subquestions → Group both.
- Do a final check if i missed anything 

Output:
[
  ["List of units","grouped by their respective region", "unit_hier"]
]

Examples 2 

user_query: "Give me the list of units who have completed the assigned project on time. List should be grouped by their respective regions."
table_desc = [project : It contain the data about the projects assigned to units in the company."]

HOW TO THINK STEP BY STEP:
- Understand the CONTEXT and business process.
- “List of units  → Check if any table tracks units → No, ignore this subquestion. 
- “select project completed on time” → Check for completed project. → Yes, "project" table.  Check if any table is needed that has link with project identifier and helps in answering user question
- “grouped by their respective region.” → Check if any table tracks employee → No, ignore this subquestion. 
- Do a final check if i missed anything 

Output:
[
  ["select project completed on time", "project"],
]

"""

human_message_content ="""Given the user question and table description, generate subquestions along with their corresponding table names as per the instructions above.
User Question: {user_query}
Table Description: {table_desc}
"""

task1 = RunnableLambda(lambda x: x["user_query"])
task2 = RunnableLambda(lambda x: x["table_desc"])

final_task = RunnableMap({
    "user_query": task1,   
    "table_desc": task2
})

# Wrap the chain with logging
def generate_subquestions_with_logging(inputs):
    print(f"  [SUBQUESTION CHAIN] Processing user query and table descriptions...")
    
    # ✅ Extract agent_system_message from inputs
    agent_system_message = inputs.get("agent_system_message", "")
    
    try:
        # ✅ Create prompt dynamically with agent context
        prompt = getPrompt(system_message_content, human_message_content, agent_system_message)
        
        chain = final_task | prompt | llm | StrOutputParser()
        time.sleep(10)
        result = chain.invoke(inputs)
        print(f"  [SUBQUESTION CHAIN] [SUCCESS] Subquestions generated successfully")
        return result
    except Exception as e:
        print(f"  [SUBQUESTION CHAIN] [ERROR] {str(e)}")
        raise

generate_subquestions_chain = RunnableLambda(generate_subquestions_with_logging)

