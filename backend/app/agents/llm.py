import os
from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    # Make sure OPENAI_API_KEY is in your environment variables.
    # We use temperature=0 for deterministic outputs required for coding tasks.
    return ChatOpenAI(model="gpt-4-turbo", temperature=0)
