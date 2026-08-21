\# Local RAG Assistant



A local Retrieval-Augmented Generation (RAG) assistant built with \*\*Microsoft Foundry Local\*\*, \*\*Streamlit\*\*, and \*\*SQLite\*\*.



The application allows users to upload documents and ask questions about their content. The system retrieves relevant information from the local knowledge base and uses a local language model to generate answers.



\## Features



\* 📄 TXT document support

\* 📖 PDF document support

\* 📘 DOCX document support

\* 📙 PPTX document support

\* 🧩 Document chunking

\* 🔢 Text embeddings with Qwen3-Embedding-0.6B

\* 🔎 Semantic search using cosine similarity

\* 🗄️ SQLite-based local knowledge base

\* 🤖 Local answer generation with Phi-3.5-mini

\* 📴 Local/offline AI inference

\* 💬 Streamlit chat interface

\* 📚 Document source tracking



\## How It Works



The application follows a standard RAG pipeline:



```text

Document

&#x20;  ↓

Text Extraction

&#x20;  ↓

Chunking

&#x20;  ↓

Qwen3-Embedding-0.6B

&#x20;  ↓

Vector Embeddings

&#x20;  ↓

SQLite Knowledge Base

&#x20;  ↓

User Question

&#x20;  ↓

Query Embedding

&#x20;  ↓

Cosine Similarity Search

&#x20;  ↓

Relevant Chunks

&#x20;  ↓

Phi-3.5-mini

&#x20;  ↓

Generated Answer

```



\### 1. Document Processing



When a document is uploaded, the application extracts its text.



Supported formats:



\* TXT

\* PDF

\* DOCX

\* PPTX



\### 2. Chunking



The extracted text is divided into smaller sections called \*\*chunks\*\*.



This makes it possible to search the document content more efficiently.



\### 3. Embeddings



Each chunk is converted into a numerical vector using:



\*\*Qwen3-Embedding-0.6B\*\*



These vectors represent the semantic meaning of the text.



\### 4. Retrieval



When the user asks a question, the question is also converted into an embedding.



The system compares the question vector with stored document vectors using \*\*cosine similarity\*\* and retrieves the most relevant chunks.



\### 5. Answer Generation



The retrieved chunks are provided as context to:



\*\*Phi-3.5-mini\*\*



The model generates an answer based on the retrieved local information.



The system is instructed not to use outside knowledge when answering document-based questions.



\## Technologies



| Technology              | Purpose                        |

| ----------------------- | ------------------------------ |

| Python                  | Application development        |

| Streamlit               | Web interface                  |

| Microsoft Foundry Local | Local AI model execution       |

| Phi-3.5-mini            | Answer generation              |

| Qwen3-Embedding-0.6B    | Text embeddings                |

| SQLite                  | Local knowledge base           |

| PyPDF                   | PDF text extraction            |

| python-docx             | Word document extraction       |

| python-pptx             | PowerPoint document extraction |



\## Project Structure



```text

local-rag-assistant/

│

├── app.py

├── chunker.py

├── embedder.py

├── generator.py

├── retriever.py

├── vector\_store.py

├── requirements.txt

├── .gitignore

└── README.md

```



\## Installation



Clone the repository:



```bash

git clone https://github.com/nurullahciftci-2004/local-rag-assistant.git

cd local-rag-assistant

```



Install the required Python packages:



```bash

pip install -r requirements.txt

```



Make sure \*\*Microsoft Foundry Local\*\* is installed and the required local models are available.



\## Running the Application



Start the Streamlit application:



```bash

streamlit run app.py

```



The application will open in the browser.



\## Supported Documents



The application currently supports:



| Format | Support |

| ------ | ------- |

| TXT    | ✅       |

| PDF    | ✅       |

| DOCX   | ✅       |

| PPTX   | ✅       |



\## Privacy and Local Processing



The project is designed around local document processing and local model inference.



Uploaded documents and the local SQLite knowledge base are kept outside the Git repository through `.gitignore`.



The repository therefore does not contain the user's local documents or database.



\## Example



A user can upload a PowerPoint presentation such as:



```text

Chapter 10 Managing Work Groups and Work Teams.pptx

```



and ask:



```text

What is the difference between a work group and a work team?

```



The system retrieves relevant information from the presentation and generates an answer using the local language model.



\## Project Purpose



This project was developed as an internship project to demonstrate the practical use of:



\* Retrieval-Augmented Generation

\* Local Large Language Models

\* Text embeddings

\* Semantic search

\* Document processing

\* Local knowledge bases



\## Author



\*\*Nurullah Çiftci\*\*

\*\*Istinye Universtiy / Management Information Systems\*\*



2026



