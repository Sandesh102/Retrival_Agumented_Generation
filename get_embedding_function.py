from langchain_community.embeddings import FastEmbedEmbeddings


def get_embedding_function():
    embeddings = FastEmbedEmbeddings()
    return embeddings
