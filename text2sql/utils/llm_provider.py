import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
gcpApiKey = os.getenv('GOOGLE_API_KEY')
print(f"[LLM PROVIDER] Loaded GOOGLE_API_KEY from .env {gcpApiKey[:10]}")
if not gcpApiKey:
    raise RuntimeError("GOOGLE_API_KEY not found in environment variables. Please set it in the .env file.")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=gcpApiKey, temperature=0)