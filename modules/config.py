import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

DATA_DIR = "data"
VECTORSTORE_DIR = "vectorstore"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

TOP_K = 8