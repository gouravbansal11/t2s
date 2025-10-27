import pandas as pd

from langchain_core.messages import HumanMessage , SystemMessage    
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import  RunnableMap,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

load_dotenv()

# Loading the key
gcpApiKey = os.getenv('GOOGLE_API_KEY')
print(gcpApiKey)

# Manually Table Descriptions

tables_descriptions = {
    'POC_UNIT_HIER' : ''' It contain the data about the units/store hierarchy. This also have the unit information.''',
   # 'POC_PROJECT' : ''' It contains the data about the projects, including project. One Project is assigned to one or multiple units/stores.''',
   # 'POC_PROJ_EXECUTION' : ''' It contains the data about the projects executions. When any project assigned to any unit. One instance is 
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

# Creating message for the LLM to generate the table description and column description

system_message = SystemMessage(content="""You are an expert in database design and documentation. Your task is to analyze the structure and data of SQL tables, along with their descriptions, and generate concise yet comprehensive descriptions for each table and its columns.
                                These descriptions will act as a knowledge base for a text-to-SQL converter system to better understand the purpose and context of the tables and their columns. """);

human_message = HumanMessage(content="""Given the table name, its description, and a sample of its data, generate a concise yet comprehensive description for the table and its columns.
                                        Donot add the generic statement or description. Here are the details:
                                        Table Name: {table_name}
                                        Table Description: {table_description}
                                        Sample Data: {sample_data}
                                        
                                        OutPut should be in Map format, 
                                        where first key is the <table_name>_description and value is actual table description.
                                        Another key would be columns_names_description and value would be column description.        
                            """)

# LLM Model object creation and invoking
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=gcpApiKey, temperature=0)
prompt = ChatPromptTemplate.from_messages([system_message, human_message])

task_one = RunnableLambda(lambda x : x["table_description"])
task_two = RunnableLambda(lambda x : x["sample_data"])

final_task = RunnableMap({
    "table_description": task_one,
    "sample_data": task_two,
})

# Creating Lang Chain
chain = final_task | prompt | llm | StrOutputParser()


# Generating the knowledgebase  for the tables
metadata={}
for key,value in tables_descriptions.items():
    sample_data = fetch_data(key)
    result = chain.invoke({
        "table_name": key,
        "table_description": value,
        "sample_data": sample_data.to_dict(orient='records')
    })
    print(f"For Table {key} the description is {result}")
    metadata[key] = result



