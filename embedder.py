from foundry_local_sdk import Configuration, FoundryLocalManager
from chunker import chunk_text
from vector_store import create_database, save_embedding
from pathlib import Path
import sqlite3


DATABASE_PATH = "rag_database.db"


def clear_database():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM documents")

    connection.commit()
    connection.close()


def main():

    # 1. Veritabanını hazırla
    create_database()
    clear_database()

    # 2. Foundry Local SDK'yi başlat
    config = Configuration(
        app_name="foundry_local_rag"
    )

    FoundryLocalManager.initialize(config)

    manager = FoundryLocalManager.instance

    # 3. Documents klasöründeki tüm TXT dosyalarını bul
    documents_folder = Path("documents")

    document_files = list(
        documents_folder.glob("*.txt")
    )

    if not document_files:
        print("Documents klasöründe .txt dosyası bulunamadı.")
        return

    print(
        f"{len(document_files)} document bulundu."
    )
    print()

    # 4. Embedding modelini hazırla
    embedding_model = manager.catalog.get_model(
        "qwen3-embedding-0.6b"
    )

    print("Embedding modeli hazırlanıyor...")

    embedding_model.download(
        lambda progress: print(
            f"\rDownloading: {progress:.1f}%",
            end="",
            flush=True,
        )
    )

    print()

    embedding_model.load()

    print("Embedding model loaded successfully.")
    print()

    # 5. Embedding client oluştur
    embedding_client = (
        embedding_model.get_embedding_client()
    )

    total_chunks = 0

    # 6. Her dokümanı işle
    for document_path in document_files:

        print("=" * 70)
        print(f"Processing: {document_path}")
        print("=" * 70)

        # Dokümanı oku
        text = document_path.read_text(
            encoding="utf-8"
        )

        # Chunk'lara ayır
        chunks = chunk_text(text)

        print(
            f"Total chunks: {len(chunks)}"
        )
        print()

        # Chunk'ları embedding'e çevir
        for i, chunk in enumerate(
            chunks,
            start=1
        ):

            response = (
                embedding_client.generate_embedding(
                    chunk
                )
            )

            vector = (
                response.data[0].embedding
            )

            save_embedding(
                source=str(document_path),
                chunk_id=i,
                content=chunk,
                embedding=vector,
            )

            print(
                f"Chunk {i}: "
                f"{len(vector)} dimensions "
                f"→ saved to database"
            )

            total_chunks += 1

        print()

    # 7. Modeli kapat
    embedding_model.unload()

    print("=" * 70)
    print("All embeddings generated successfully!")
    print(f"Documents processed: {len(document_files)}")
    print(f"Total chunks: {total_chunks}")
    print("=" * 70)


if __name__ == "__main__":
    main()