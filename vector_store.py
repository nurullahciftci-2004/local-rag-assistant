import sqlite3
import json


DATABASE_PATH = "rag_database.db"


def create_database():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            chunk_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_embedding(source, chunk_id, content, embedding):
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO documents
        (source, chunk_id, content, embedding)
        VALUES (?, ?, ?, ?)
        """,
        (
            source,
            chunk_id,
            content,
            json.dumps(embedding),
        ),
    )

    connection.commit()
    connection.close()


def get_all_documents():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, source, chunk_id, content, embedding
        FROM documents
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


if __name__ == "__main__":
    create_database()

    print("Vector database created successfully!")
    print(f"Database: {DATABASE_PATH}")