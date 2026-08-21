from foundry_local_sdk import Configuration, FoundryLocalManager
from retriever import search


def main():
    print("Foundry Local başlatılıyor...")

    config = Configuration(
        app_name="rag-assistant",
        model_cache_dir=r"C:\Users\nurll\.foundry\cache\models"
    )

    FoundryLocalManager.initialize(config)

    manager = FoundryLocalManager.instance

    # --------------------------------------------------
    # Embedding Model
    # --------------------------------------------------

    print("Embedding modeli yükleniyor...")

    embedding_model = manager.catalog.get_model(
        "qwen3-embedding-0.6b"
    )

    embedding_model.load()

    print("Embedding modeli yüklendi.")

    embedding_client = embedding_model.get_embedding_client()

    # --------------------------------------------------
    # Chat Model
    # --------------------------------------------------

    print("Chat modeli yükleniyor...")

    generation_model = manager.catalog.get_model(
        "phi-3.5-mini"
    )

    generation_model.load()

    print("Chat modeli yüklendi.")

    chat_client = generation_model.get_chat_client()

    # --------------------------------------------------
    # RAG Chat Loop
    # --------------------------------------------------

    print()
    print("=" * 70)
    print("LOCAL RAG ASSISTANT")
    print("=" * 70)
    print("Ask questions about the documents.")
    print("Type 'exit' to quit.")
    print("=" * 70)

    while True:

        print()
        question = input("Your question: ")

        # Exit command
        if question.lower().strip() == "exit":
            print()
            print("Goodbye!")
            break

        # Empty question check
        if not question.strip():
            print("Please enter a question.")
            continue

        print()
        print("Relevant information is being retrieved...")

        # --------------------------------------------------
        # Retrieval
        # --------------------------------------------------

        results = search(
            question,
            embedding_client,
            top_k=3
        )

        # --------------------------------------------------
        # Show Retrieved Documents
        # --------------------------------------------------

        print()
        print("=" * 70)
        print("RETRIEVED DOCUMENTS")
        print("=" * 70)

        for i, result in enumerate(results, start=1):
            print(f"\n[{i}] Source: {result['source']}")
            print(f"    Chunk: {result['chunk_id']}")
            print(f"    Similarity: {result['score']:.4f}")
            print(f"    Content: {result['content'][:300]}...")

        print("=" * 70)

        # --------------------------------------------------
        # Create Context
        # --------------------------------------------------

        context_parts = []

        for result in results:
            context_parts.append(
                f"Source: {result['source']}\n"
                f"Chunk: {result['chunk_id']}\n"
                f"Similarity: {result['score']:.4f}\n"
                f"Content:\n{result['content']}"
            )

        context = "\n\n".join(context_parts)

        # --------------------------------------------------
        # RAG Prompt
        # --------------------------------------------------

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful travel assistant. "
                    "Answer the user's question using ONLY "
                    "the information provided in the context. "
                    "If the context does not contain enough "
                    "information, say so."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n\n{context}\n\n"
                    f"Question: {question}"
                )
            }
        ]

        # --------------------------------------------------
        # Generate Answer
        # --------------------------------------------------

        print()
        print("Generating answer...")
        print()

        response = chat_client.complete_chat(messages)

        print("=" * 70)
        print("RAG ANSWER")
        print("=" * 70)
        print(response.choices[0].message.content)
        print("=" * 70)

    # --------------------------------------------------
    # Unload Models
    # --------------------------------------------------

    generation_model.unload()
    embedding_model.unload()


if __name__ == "__main__":
    main()