from langchain_core.runnables import  RunnableLambda,RunnableMap
from langchain_google_genai import  ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

system_message = SystemMessage(content="""You are an part of text to sql convertor. In this System we have multiple agents responsible for their own work.
                Based on the user query, Your work is to identify which agent is best suited to handle the query.
                Below are the agents and their responsibilities:
                    unit agent: Handles queries related to unit/store information and hierarchy.
                    project agent: Handles queries related to projects & their executions and their assignments to units/stores.
                    user agent: Handles queries related to users, their roles, and permissions within the system.
                When you receive a user query, analyze its content and determine which agent is most appropriate to address the query.
                If the query is related to unit/store information or hierarchy and also related to project, then return {"unit","project"}
                If the query is related to user information, then return {"user"}
                If the query is related to unit,user,project information, then return {"user","unit","project"}
                """)

human_message = HumanMessage(content="""Given the query {user_query} , identify the best suited agent to handle the query.""")

prompt = ChatPromptTemplate.from_messages([system_message, human_message])
llm = ChatGoogleGenerativeAI(model="gemini-pro")

task = RunnableLambda(lambda x : x["user_query"])

final_task = RunnableMap({
    "user_query": task,
    })

chain = final_task | prompt | llm | StrOutputParser

def router_agent(query: str):
    result = chain.invoke({"user_query":query})
    return {"router_agent_response":result}


