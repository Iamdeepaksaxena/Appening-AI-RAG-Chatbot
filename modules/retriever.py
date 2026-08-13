from modules import config


def get_retriever(db):
    return db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": config.TOP_K
        }
    )