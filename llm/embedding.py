from sentence_transformers import SentenceTransformer


def setup_embedding(embedding_model:str):
    # Load the embedding model
    # model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
    model = SentenceTransformer(embedding_model, trust_remote_code=True)

    # Define a function to generate embeddings
    # def get_embedding(data, precision="float32"):
    # return model.encode(data, precision=precision).tolist()
    # Generate an embedding
    # embedding = model.encode(data, precision=precision).tolist()
    # # print(embedding)
    # return embedding
    return model

def get_embedding(model: SentenceTransformer, data:str):
    return model.encode(data, precision="float32").tolist() 