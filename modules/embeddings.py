from langchain_huggingface import HuggingFaceEmbeddings
from modules import config


def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        encode_kwargs={
            "normalize_embeddings": True
        }
    )