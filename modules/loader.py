import os
from langchain_community.document_loaders import PyPDFLoader
from modules import config


def load_documents():
    documents = []
    for filename in os.listdir(config.DATA_DIR):
        if not filename.lower().endswith(".pdf"):
            continue
        filepath = os.path.join(
            config.DATA_DIR,
            filename
        )

        loader = PyPDFLoader(filepath)
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = filename
        documents.extend(docs)
        print(f"Loaded {filename}")
    print(f"Loaded {len(documents)} pages")
    return documents