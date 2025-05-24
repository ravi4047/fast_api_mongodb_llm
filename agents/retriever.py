from langchain.agents.agent_toolkits import create_retriever_tool

from langchain_mongodb.retrievers import (
    MongoDBAtlasParentDocumentRetriever,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

### When do I need a retriever stuff. Probably 

def setup_retriever_tool():
    _ = vector_store.add_texts(artists + albums)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    description = (
        "Use to look up values to filter on. Input is an approximate spelling "
        "of the proper noun, output is valid proper nouns. Use the noun most "
        "similar to the search."
    )
    retriever_tool = create_retriever_tool(
        retriever,
        name="search_proper_nouns",
        description=description,
    )
    return retriever_tool

# from langchain_openai import OpenAIEmbeddings

# embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
# from langchain_community.embeddings import HuggingFaceEmbeddings ## ❌❌ This is outdated I think
from langchain_huggingface import HuggingFaceEmbeddings
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") 

### Byte Pair encoding

# DB_NAME = "langchain"
# COLLECTION_NAME = "parent_doc"


def get_splitter(chunk_size: int) -> RecursiveCharacterTextSplitter:
    """
    Returns a token-based text splitter with overlap
    Args:
        chunk_size (_type_): Chunk size in number of tokens
    Returns:
        RecursiveCharacterTextSplitter: Recursive text splitter object
    """
    # return RecursiveCharacterTextSplitter.from_huggingface_tokenizer(

    # )

    return RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=chunk_size,
        chunk_overlap=0.15 * chunk_size,
    )