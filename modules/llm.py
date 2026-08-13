from langchain_groq import ChatGroq
from modules import config
 
 
def get_llm():
    return ChatGroq(
        api_key=config.GROQ_API_KEY,
        model=config.GROQ_MODEL,
        temperature=0,
    )
 