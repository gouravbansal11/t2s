# Text2SQL - Natural Language to SQL Conversion System

A production-ready multi-agent system that transforms natural language queries into optimized SQL queries with intelligent data visualization recommendations.

**System Type:** Multi-Agent LangGraph Pipeline  
**LLM:** Google Gemini 2.5 Flash  
**Database:** PostgreSQL with fact & dimension tables  
**Framework:** LangGraph, Python, Pydantic

---

## 📖 Table of Contents

1. [Quick Start](#quick-start)
2. [Project Overview](#project-overview)
3. [System Architecture](#system-architecture)
4. [API Components](#api-components)
5. [Testing & Examples](#testing--examples)
6. [Demo Video](#demo-video)

---

## Quick Start

### Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate metadata (one-time setup)
python knowledgebaseAgent.py

# 3. Run the pipeline
python main.py

# Expected output:
# [ROUTER] Analyzing query...
# [TABLE EXTRACTOR] Processing tables...
# [FILTER CHECK] Validating filters...
# [SQL GENERATOR] Generating SQL...
# [UI SELECTOR] Recommending visualization...
# [SUCCESS] SQL and visualization ready
```

### Testing the System

```bash
# Run with a sample query
python main.py

# Example queries to try:
# - "How many projects do we have?"
# - "Give me count of projects by status"
# - "Show projects by status for store level units"
# - "List all active projects with their status"
```

---

## Project Overview

### What This System Does

Text2SQL is a **multi-agent text-to-SQL conversion pipeline** that:

1. **Understands natural language queries** - Parses user intent and business context
2. **Routes to specialized agents** - Matches queries to relevant data tables
3. **Extracts relevant data** - Identifies tables, columns, and filter conditions  
4. **Validates filters** - Ensures filter conditions are valid and applicable
5. **Generates SQL** - Creates optimized database queries
6. **Recommends visualizations** - Suggests best UI components for results

### Key Features

✅ **Multi-Agent Architecture** - Parallel execution of specialized agents  
✅ **Intelligent Routing** - Dynamic agent selection based on query intent  
✅ **Filter Validation** - 6-step validation process to prevent errors  
✅ **Flexible Output** - Multiple visualization types (table, bar, line, pie, scatter, heatmap)  
✅ **Graceful Degradation** - Continues processing even when components fail  
✅ **Type-Safe** - Pydantic models for data validation at each stage

---

## System Architecture

### Pipeline Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                TEXT-TO-SQL CONVERSION PIPELINE                   │
└──────────────────────────────────────────────────────────────────┘

                    🚀 User Natural Language Query
                               │
                               ▼
                    ┌──────────────────────┐
                    │  1️⃣ ROUTER AGENT   │
                    │ (Identify tables)    │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
        ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
        │ Unit Hier   │  │  Project     │  │  Dimension   │
        │  Agent      │  │   Agent      │  │   Agent      │
        └────┬────────┘  └──────┬───────┘  └──────┬───────┘
             │                  │                 │
             └──────────────────┼─────────────────┘
                                │ (Parallel Execution)
                    ┌───────────▼──────────┐
                    │ TABLE EXTRACTION     │
                    │ • Subquestions       │
                    │ • Column names       │
                    │ • 3-layer validation │
                    └───────────┬──────────┘
                                │
                    ┌───────────▼──────────┐
                    │ 2️⃣ FILTER CHECK    │
                    │ • Validate filters   │
                    │ • 6-step analysis    │
                    └───────────┬──────────┘
                                │
                    ┌───────────▼──────────┐
                    │ 3️⃣ SQL GENERATOR   │
                    │ • Build schema       │
                    │ • Generate SQL query │
                    └───────────┬──────────┘
                                │
                    ┌───────────▼──────────┐
                    │ 4️⃣ UI SELECTOR     │
                    │ • Analyze results    │
                    │ • Recommend chart    │
                    └───────────┬──────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │ 📊 FINAL OUTPUT      │
                    │ ✓ SQL Query          │
                    │ ✓ Visualization Type │
                    │ ✓ Configuration      │
                    └──────────────────────┘
```

### Data State Transformation

The system passes data through **AgentState** object with these fields:

```python
class AgentState(BaseModel):
    user_query: str                 # Input: User's natural language query
    router_response: list[str]      # Router's selected agents
    subquestions: dict              # Extracted subquestions from all agents
    selected_columns: dict          # Extracted columns from all agents  
    filters: list                   # Validated filter conditions
    generated_sql_query: str        # Final SQL query
    ui_components: dict             # UI component recommendations
```

**Example State Transformation:**

```
Stage 0: INPUT
├─ user_query: "Count of projects by status for store level units"
└─ [other fields empty]

Stage 1: ROUTING → Add router response
├─ router_response: ["project_agent", "dimension_agent", "unit_hier_agent"]

Stage 2: TABLE EXTRACTION → Add extracted data
├─ subquestions: {"project_agent": [...], "dimension_agent": [...], ...}
├─ selected_columns: {"project_agent": [...], "dimension_agent": [...], ...}

Stage 3: FILTER VALIDATION → Add validated filters
├─ filters: ["yes", ["POC_UNIT_HIER", "unit_org_level", 5]]

Stage 4: SQL GENERATION → Add SQL query
├─ generated_sql_query: "SELECT ... FROM POC_PROJECT JOIN POC_STATUS_D ..."

Stage 5: UI SELECTION → Add visualization recommendation
├─ ui_components: {"recommended_component": "bar_chart", ...}
```

---

## API Components

### 1. Router Agent (routerAgent.py)

**Purpose:** Analyze query and route to appropriate specialized agents

**Input:**
```
user_query: "How many projects by status?"
```

**Output:**
```
router_response: ["project_agent", "dimension_agent"]
```

**Logic:**
- Matches keywords in query to table names
- Selects agents that own relevant tables
- Handles multi-table queries with parallel execution

---

### 2. Table Extraction Agents (tables_agents/)

Three specialized agents work in parallel to extract relevant data:

#### Unit Hierarchy Agent
- **Tables:** POC_UNIT_HIER
- **Role:** Extract organizational hierarchy queries
- **Output:** Subquestions + column names

#### Project Agent
- **Tables:** POC_PROJECT, POC_PROJECT_EXECUTION
- **Role:** Extract project-related queries
- **Output:** Subquestions + column names

#### Dimension Agent
- **Tables:** POC_STATUS_D (and other dimension tables)
- **Role:** Extract dimension lookup queries
- **Output:** Subquestions + column names

**Processing:**
1. Receive query from router
2. Extract relevant subquestions for their tables
3. Extract column names for those tables
4. Validate data quality (3-layer validation)
5. Return results to state (merged with Annotated dict reducer)

---

### 3. Filter Check Agent (filter_check_agent.py)

**Purpose:** Validate and normalize filter conditions

**Input:**
```
columns: ["unit_org_level", "status_skey", ...]
filters: ["store level", "Q4 2024"]
```

**6-Step Validation:**
1. Understand filter context
2. Analyze syntax
3. Check data types match
4. Validate logical consistency
5. Provide recommendations
6. Clear decision (VALID/INVALID)

**Output:**
```
filters: [
  "yes",
  ["POC_UNIT_HIER", "unit_org_level", 5],
  ["POC_PROJECT", "start_date", "> 2024-10-01"]
]
```

---

### 4. SQL Generator Agent (query_generator_agent.py)

**Purpose:** Generate optimized SQL query from all context

**Input:**
```
subquestions: {...extracted data...}
selected_columns: {...column mappings...}
filters: [...validated filters...]
```

**Processing:**
1. Load table metadata from knowledgebase
2. Build dynamic schema context
3. Combine all information
4. Generate SQL with proper JOINs and WHERE clauses
5. Validate SQL syntax

**Output:**
```sql
SELECT u.unit_name, s.status_desc, COUNT(DISTINCT p.project_skey) as count
FROM POC_PROJECT p
JOIN POC_STATUS_D s ON p.status_skey = s.status_skey
JOIN POC_UNIT_HIER u ON p.creator_unit_skey = u.unit_skey
WHERE u.unit_org_level = 5
GROUP BY u.unit_name, s.status_desc
ORDER BY count DESC
```

---

### 5. UI Selector Agent (ui_selector_agent.py)

**Purpose:** Recommend best visualization for query results

**Input:**
```
user_query: "Count of projects by status"
generated_sql_query: "SELECT ... FROM POC_PROJECT JOIN POC_STATUS_D ..."
```

**Decision Logic:**

| Scenario | Chart Type |
|----------|-----------|
| Single aggregate value | Metric/Card |
| Categories vs numbers | Bar Chart |
| Time-series data | Line Chart |
| Parts of whole (%) | Pie Chart |
| Two numeric variables | Scatter Plot |
| 2D matrix/heatmap | Heatmap |
| Multiple columns/raw data | Table |

**Output:**
```json
{
  "recommended_component": "bar_chart",
  "primary_reason": "Comparing counts across status categories",
  "fields": {
    "x_axis": "status_desc",
    "y_axis": "count"
  },
  "configs": {
    "color": "steelblue",
    "alpha": 0.8
  }
}
```

---

## Testing & Examples

### Example 1: Simple Count Query

**Query:**
```
"How many projects do we have?"
```

**Processing:**
```
✓ Router identifies: project_agent
✓ Extracts tables: POC_PROJECT
✓ Selects columns: project_skey, project_name
✓ No filters required
✓ SQL: SELECT COUNT(DISTINCT project_skey) FROM POC_PROJECT
✓ Recommended UI: Metric card
```

### Example 2: Category Comparison

**Query:**
```
"Count of projects by status"
```

**Processing:**
```
✓ Router identifies: project_agent, dimension_agent
✓ Extracts tables: POC_PROJECT, POC_STATUS_D
✓ Selects columns: project_skey, status_skey, status_desc
✓ No filters required
✓ SQL: SELECT status_desc, COUNT(*) FROM POC_PROJECT 
       JOIN POC_STATUS_D USING (status_skey) GROUP BY status_desc
✓ Recommended UI: Bar chart
```

### Example 3: Complex Multi-Join with Filters

**Query:**
```
"Count of active projects by status for store level units in Q4"
```

**Processing:**
```
✓ Router identifies: project_agent, dimension_agent, unit_hier_agent
✓ Parallel table extraction from 3 agents
✓ Filter validation:
  - "active" → filter on status = 'ACTIVE'
  - "store level" → filter on unit_org_level = 5
  - "Q4" → filter on QUARTER(start_date) = 4
✓ SQL combines all JOINs and filters
✓ Recommended UI: Bar chart with grouping
```

### Running Tests

```bash
# Test with predefined queries
python main.py

# Try these queries:
queries = [
    "How many projects?",
    "Projects by status",
    "Active projects by unit",
    "Project count by month",
    "Show all project details",
]
```

---

## 📹 Demo Video

Watch the complete Text-to-SQL system in action!

<video width="100%" controls style="max-width: 800px; border: 2px solid #333; border-radius: 8px;">
  <source src="TextToSQL_Convertor_Demo.avi" type="video/x-msvideo">
  Your browser doesn't support AVI video playback. 
  <a href="TextToSQL_Convertor_Demo.avi">Download the demo video instead</a>
</video>

**File:** `TextToSQL_Convertor_Demo.avi` (~36 MB)

### What You'll See

✅ Natural language query input  
✅ Multi-agent routing and processing  
✅ Parallel table extraction  
✅ Filter validation  
✅ Real-time SQL generation  
✅ Visualization recommendations  
✅ Dynamic charts (bar, line, pie, scatter, heatmap, table)  
✅ Complete end-to-end pipeline execution  

### Play Locally

If the browser player doesn't work:

```bash
# On Windows
start TextToSQL_Convertor_Demo.avi

# Or open with your preferred video player
```

---

## Folder Structure

```
text2sql/
├── agents/
│   ├── routerAgent.py              # Main routing logic
│   ├── tables_agents/
│   │   ├── unit_hier_agent.py      # Organizational hierarchy extraction
│   │   ├── project_agent.py        # Project data extraction
│   │   ├── dimension_agent.py      # Dimension table extraction
│   │   └── filter_check_agent.py   # Filter validation
│   └── query_generator_agents/
│       └── query_generator_agent.py # SQL generation
│
├── services/
│   └── ui_generator.py              # Visualization rendering
│
├── utils/
│   ├── llm_provider.py              # Google Gemini integration
│   ├── prompt_provider.py           # Prompt management
│   ├── db_utility.py                # Database utilities
│   └── state_reducers.py            # State merging logic
│
├── knowledgebaseAgent.py            # Metadata generation
├── main.py                          # Pipeline orchestration
├── router.py                        # State management
├── sql/
│   └── DDL.sql                      # Database schema
├── requirements.txt                 # Dependencies
└── TextToSQL_Convertor_Demo.avi    # Demo video
```

---

## Dependencies

- `langchain` - LLM framework
- `langgraph` - Multi-agent orchestration
- `google-generativeai` - Gemini API
- `pydantic` - Data validation
- `pandas` - Data processing
- `matplotlib` - Visualization
- `sqlalchemy` - Database ORM
- `python-dotenv` - Configuration

See `requirements.txt` for complete list.

---

## Configuration

Key settings are centralized in `agents/routerAgent.py`:

```python
AGENT_CONFIG = {
    "unit_hier_agent": {
        "tables": ["POC_UNIT_HIER"],
        "description": "Organizational hierarchy queries"
    },
    "project_agent": {
        "tables": ["POC_PROJECT", "POC_PROJECT_EXECUTION"],
        "description": "Project-related queries"
    },
    "dimension_agent": {
        "tables": ["POC_STATUS_D", ...],
        "description": "Dimension table queries"
    }
}
```

---

## Support

For issues or questions:
1. Check the example queries above
2. Verify database connection in configuration
3. Review agent logs for detailed error messages
4. Ensure all dependencies are installed: `pip install -r requirements.txt`

---

**Status:** ✅ Production Ready  
**Last Updated:** November 30, 2025
