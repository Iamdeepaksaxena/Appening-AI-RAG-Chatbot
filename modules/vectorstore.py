# Builds and loads the Chroma vector database.

import os
from langchain_chroma import Chroma
from modules import config
from modules.embeddings import get_embeddings


def create_vectorstore(chunks):
    embeddings = get_embeddings()
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=config.VECTORSTORE_DIR,
    )
    print("Vectorstore created")
    return db


def load_vectorstore():
    if not os.path.exists(config.VECTORSTORE_DIR):
        return None

    embeddings = get_embeddings()
    db = Chroma(
        persist_directory=config.VECTORSTORE_DIR,
        embedding_function=embeddings,
    )
    return db