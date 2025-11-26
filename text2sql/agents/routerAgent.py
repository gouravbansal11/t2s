from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_core.output_parsers import StrOutputParser
import json
from utils.llmProvider import llm
from utils.promptProvider import getPrompt

# ============================================================================
# AGENT CONFIGURATION - Source of Truth
# ============================================================================
# This is the single source of truth for all available agents.
# When you add/remove agents, update only this configuration.

AGENT_CONFIG = {
    "unit_hier_agent": {
        "display_name": "Unit Hierarchy Agent",
        "description": "Specializes in queries about stores, branches, organizational units, their hierarchy, regional groupings",
        "tables": ["POC_UNIT_HIER"],
        "keywords": ["unit", "store", "branch", "location", "hierarchy", "region", "district", "site", "address"]
    },
    "project_agent": {
        "display_name": "Project Agent",
        "description": "Specializes in queries concerning tasks, initiatives, work efforts, projects, their status, timelines, resources, execution details",
        "tables": ["POC_PROJECT", "POC_PROJECT_EXECUTION"],
        "keywords": ["project", "initiative", "execution", "status", "timeline", "assignment", "schedule", "work", "deliverable", "milestone"]
    },
    "dimension_agent": {
        "display_name": "Dimension Agent",
        "description": "Specializes in queries about lookup reference data, status descriptions, human-readable codes, and data enrichment from dimension tables",
        "tables": ["POC_STATUS_D"],
        "keywords": ["status", "description", "code", "lookup", "reference", "meaning", "what is", "explain", "human-readable"]
    },
    "user_agent": {
        "display_name": "User Agent",
        "description": "Specializes in queries about individuals, employees, users, their personal details, roles, permissions",
        "tables": [],
        "keywords": ["user", "employee", "person", "role", "permission", "access", "login", "profile", "contact", "administrator", "staff"]
    }
}

AGENT_NAME_MAPPING = {
    "unit_agent": "unit_hier_agent",
    "unit_hier_agent": "unit_hier_agent",
    "project_agent": "project_agent",
    "project": "project_agent",
    "dimension_agent": "dimension_agent",
    "dimension": "dimension_agent",
    "lookup": "dimension_agent",
    "reference": "dimension_agent",
    "status": "dimension_agent",
    "user_agent": "user_agent",
    "user": "user_agent",
    "general_inquiry": "general_inquiry"
}

def get_available_agents():
    """Returns list of currently implemented/active agents"""
    return ["unit_hier_agent", "project_agent", "dimension_agent"]

def get_agent_tables():
    """Returns mapping of agents to their database tables"""
    return {
        "unit_hier_agent": AGENT_CONFIG["unit_hier_agent"]["tables"],
        "project_agent": AGENT_CONFIG["project_agent"]["tables"],
        "dimension_agent": AGENT_CONFIG["dimension_agent"]["tables"]
    }

def map_agent_names(agent_list):
    """Map LLM output agent names to actual executable node names"""
    mapped = []
    for agent in agent_list:
        mapped_name = AGENT_NAME_MAPPING.get(agent.lower().strip(), agent)
        if mapped_name in get_available_agents():
            mapped.append(mapped_name)
    return mapped if mapped else ["unit_hier_agent"]

system_message_content = """You are an intelligent router agent within a Text-to-SQL conversion system. Your sole responsibility is to accurately determine the most relevant agent(s) to handle a given user query.

**Available agents and their domain expertise:**

*   **Unit Hierarchy Agent:** Specializes in queries about stores, branches, organizational units, their hierarchy, regional groupings.
    *   Keywords: unit, store, branch, location, hierarchy, region, district, site, address.

*   **Project Agent:** Specializes in queries concerning tasks, initiatives, work efforts, projects, their status, timelines, resources, execution details.
    *   Keywords: project, initiative, execution, status, timeline, assignment, schedule, work, deliverable, milestone.

*   **Dimension Agent:** Specializes in queries about lookup reference data, status descriptions, human-readable codes, and data enrichment.
    *   Keywords: status, description, code, lookup, reference, meaning, what is, explain, human-readable.
    *   Use when: User asks for "Show me statuses", "What does status 5 mean?", or needs enrichment data.

*   **User Agent:** Specializes in queries about individuals, employees, users, their personal details, roles, permissions.
    *   Keywords: user, employee, person, role, permission, access, login, profile, contact, administrator, staff.

**Output Format:**
Return ONLY a JSON array of agent names: ["agent_name_1", "agent_name_2"]
Valid names: "unit_hier_agent", "project_agent", "dimension_agent", "user_agent", "general_inquiry"

**Examples:**
*   "Show me stores in North region" -> ["unit_hier_agent"]
*   "What projects are assigned to Store 101?" -> ["project_agent", "unit_hier_agent"]
*   "Show project executions with status descriptions" -> ["project_agent", "dimension_agent"]
*   "What are the available status codes?" -> ["dimension_agent"]
*   "List users with Admin role" -> ["user_agent"]
"""

human_message_content = """Given the user query below, determine which agent(s) should handle it.

User Query: {user_query}

Return ONLY a JSON array of agent names."""

prompt = getPrompt(system_message_content, human_message_content)
task = RunnableLambda(lambda x: x["user_query"])
final_task = RunnableMap({"user_query": task})
chain = final_task | prompt | llm | StrOutputParser()

def router_agent(query: str):
    """Main router agent function"""
    print("\n" + "="*80)
    print("[ROUTER AGENT] Starting router agent")
    print("="*80)
    print(f"[ROUTER AGENT] Input Query: {query}")
    
    try:
        result = chain.invoke({"user_query": query})
        print(f"[ROUTER AGENT] LLM Response: {result}")
        
        try:
            llm_agents = json.loads(result.strip('```json\n').strip('\n```'))
        except:
            llm_agents = json.loads(result)
        
        mapped_agents = map_agent_names(llm_agents)
        
        print(f"[ROUTER AGENT] Original LLM output: {llm_agents}")
        print(f"[ROUTER AGENT] Mapped to node names: {mapped_agents}")
        print(f"[ROUTER AGENT] [SUCCESS] Router agent completed successfully")
        print("="*80 + "\n")
        
        return {
            "router_agent_response": result,
            "mapped_agents": mapped_agents
        }
    
    except Exception as e:
        print(f"[ROUTER AGENT] [ERROR] Error during routing: {str(e)}")
        print("="*80 + "\n")
        raise
