from pathlib import Path


def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def main():
    document_path = Path("documents/paris.txt")

    text = document_path.read_text(encoding="utf-8")

    chunks = chunk_text(text)

    print(f"Document loaded: {document_path}")
    print(f"Total chunks: {len(chunks)}")
    print()

    for i, chunk in enumerate(chunks, start=1):
        print(f"--- Chunk {i} ---")
        print(chunk)
        print()


if __name__ == "__main__":
    main()