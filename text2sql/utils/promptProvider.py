from langchain.prompts import SystemMessagePromptTemplate,HumanMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate

def getPrompt(system_message_content: str, human_message_content: str) -> ChatPromptTemplate:
    system_message = SystemMessagePromptTemplate.from_template(system_message_content)
    human_message = HumanMessagePromptTemplate.from_template(human_message_content)
    prompt = ChatPromptTemplate.from_messages([system_message, human_message])    
    return prompt