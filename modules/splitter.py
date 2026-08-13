from langchain_text_splitters import RecursiveCharacterTextSplitter
from modules import config

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n","\n",". "," ",""]
    )

    chunks = splitter.split_documents(documents)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
    print(f"Created {len(chunks)} chunks")
    return chunks