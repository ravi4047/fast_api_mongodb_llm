from pymongo import UpdateOne
from llm.embedding import get_embedding
from sentence_transformers import SentenceTransformer

# https://www.mongodb.com/docs/atlas/atlas-vector-search/create-embeddings/#generate-the-embeddings-and-update-your-documents-in-.
def update_documents_embeddings(documents: list[str], embedding_model: SentenceTransformer):
    from pymongo import UpdateOne
    # Generate the list of bulk write operations
    operations = []
    for doc in documents:
        summary = doc["summary"]
        # Generate embeddings for this document
        embedding = get_embedding(summary)
        # Uncomment the following line to convert to BSON vectors
        # embedding = generate_bson_vector(embedding, BinaryVectorDtype.FLOAT32)
        # Add the update operation to the list
        operations.append(UpdateOne(
            {"_id": doc["_id"]},
            {"$set": {
                "embedding": embedding
            }}
        ))
    # Execute the bulk write operation
    if operations:
        result = collection.bulk_write(operations)
        updated_doc_count = result.modified_count
    print(f"Updated {updated_doc_count} documents.")