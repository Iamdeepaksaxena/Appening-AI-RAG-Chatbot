# Run this file to chat with your documents.

from modules.loader import load_documents
from modules.splitter import split_documents
from modules.vectorstore import create_vectorstore, load_vectorstore
from modules.retriever import get_retriever
from modules.llm import get_llm
from modules.graph import build_graph

# Step 1: get the vectorstore (load existing one, or build a new one)
db = load_vectorstore()

if db is None:
    documents = load_documents()
    chunks = split_documents(documents)
    db = create_vectorstore(chunks)

# Step 2: set up retriever, llm, and the graph
retriever = get_retriever(db)
llm = get_llm()
app = build_graph(retriever, llm)

# Step 3: simple chat loop
print("\nAsk questions about your documents. Type 'exit' to quit.\n")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break

    result = app.invoke({"question": question, "context": "", "reasoning": "", "answer": ""})

    print("\nReasoning:", result["reasoning"])
    print("Answer:", result["answer"], "\n")