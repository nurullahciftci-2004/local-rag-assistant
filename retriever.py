import sqlite3
import json
import math

from foundry_local_sdk import Configuration, FoundryLocalManager


DATABASE_PATH = "rag_database.db"


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def load_documents():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT source, chunk_id, content, embedding
        FROM documents
        """
    )

    rows = cursor.fetchall()

    connection.close()

    documents = []

    for source, chunk_id, content, embedding in rows:

        documents.append(
            {
                "source": source,
                "chunk_id": chunk_id,
                "content": content,
                "embedding": json.loads(embedding),
            }
        )

    return documents


def search(
    query,
    embedding_client,
    top_k=3,
    similarity_threshold=0.35
):

    # Convert user query to embedding

    response = embedding_client.generate_embedding(query)

    query_vector = response.data[0].embedding

    documents = load_documents()

    results = []

    for document in documents:

        score = cosine_similarity(
            query_vector,
            document["embedding"],
        )

        # Similarity threshold

        if score >= similarity_threshold:

            results.append(
                {
                    "source": document["source"],
                    "chunk_id": document["chunk_id"],
                    "content": document["content"],
                    "score": score,
                }
            )

    # Sort by similarity

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]


def main():

    config = Configuration(
        app_name="foundry_local_rag"
    )

    FoundryLocalManager.initialize(config)

    manager = FoundryLocalManager.instance

    embedding_model = manager.catalog.get_model(
        "qwen3-embedding-0.6b"
    )

    embedding_model.load()

    embedding_client = (
        embedding_model.get_embedding_client()
    )

    query = "What can I visit in Paris?"

    print(f"Query: {query}")
    print()
    print("Searching...")
    print()

    results = search(
        query,
        embedding_client,
        top_k=3,
        similarity_threshold=0.35,
    )

    if not results:

        print(
            "No relevant information was found."
        )

    else:

        for result in results:

            print(
                f"Chunk {result['chunk_id']} "
                f"| Similarity: "
                f"{result['score']:.4f}"
            )

            print(result["content"])

            print("-" * 70)

    embedding_model.unload()


if __name__ == "__main__":
    main()