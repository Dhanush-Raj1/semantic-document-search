<h1 align="center">🛍️ Semantic Document Search Engine</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=black&labelColor=white&color=red">
  <img src="https://img.shields.io/badge/FastAPI-009688-?style=for-the-badge&logo=FastAPI&logoColor=black&labelColor=white&color=purple">
  <img src="https://img.shields.io/badge/HTML-E44D26?style=for-the-badge&logo=html5&logoColor=black&labelColor=white&color=green">
  <img src="https://img.shields.io/badge/CSS-663399?style=for-the-badge&logo=CSS&logoColor=black&labelColor=white&color=orange">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=black&labelColor=white&color=cyan" />
</p>
  
<h3 align="center"> 
  A backend search engine that finds the most relevant documents for a user query using **custom TF-IDF vectorization** and **Cosine Similarity**.
</h3>

---

## 🚀 Live Applicaiton
🌐 The application is deployed and live  
  
👉 [Access the web app here](https://product-search-agent-project.onrender.com)  
  
> [!NOTE]  
> The web app may take 1-2 minutes to load.  
  
> [!TIP]  
> For the best experience, please refer to the [Usage Guide](#-usage-guide) section below to learn how to navigate and use the web app effectively.
  
<br>


## How It Works

### TF-IDF Vectorization

Every document and query is converted into a numerical vector using two components:

**Term Frequency (TF)** measures how often a word appears in a document, normalized by document length:

```
TF(term, doc) = count of term in doc / total terms in doc
```

**Inverse Document Frequency (IDF)** rewards rare, meaningful terms and down-weights common ones:

```
IDF(term) = log((N + 1) / (df + 1)) + 1
```

where `N` = total documents and `df` = number of documents containing the term.

**TF-IDF** = TF × IDF — gives each term a weight reflecting how informative it is for a specific document.

### Cosine Similarity

The similarity between the query vector and each document vector is:

```
cosine(A, B) = dot(A, B) / (|A| × |B|)
```

A score of `1.0` means perfect match; `0.0` means no shared vocabulary. All documents are scored and the top 3 are returned.

---

## Project Structure

```
semantic-search/
├── documents/          ← corpus of .txt files
├── src/
│   ├── utils.py        ← tokenization and stop word filtering
│   ├── indexer.py      ← TF-IDF logic and DocumentIndex class
│   ├── searcher.py     ← cosine similarity and ranking
│   ├── models.py       ← Pydantic response models
│   └── main.py         ← FastAPI app with all endpoints
├── static/
│   └── index.html      ← search UI
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- pip

### 1. Clone the repository

```bash
git clone <repository-url>
cd semantic-search
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add documents

Place `.txt` files in the `documents/` folder. The engine reads all `.txt` files from this directory automatically.

### 5. Start the server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The TF-IDF index is built automatically at startup.

---

## Usage

### Search UI

Open your browser and go to:

```
http://localhost:8000
```

Type a query, press **Search** or hit **Enter**. The top 3 matching documents are shown with their similarity scores and a text snippet.

To reprocess the documents folder after adding new files, click **Rebuild Index**.

### API Endpoints

#### `GET /search?q=<query>`

Search the document corpus and return the top 3 most relevant results.

**Parameters:**

| Parameter | Type   | Required | Description      |
|-----------|--------|----------|------------------|
| `q`       | string | Yes      | The search query |

**Example:**

```bash
curl "http://localhost:8000/search?q=artificial+intelligence+in+finance"
```

**Response:**

```json
{
  "query": "artificial intelligence in finance",
  "results": [
    {
      "document": "finance_ai.txt",
      "score": 0.3821,
      "snippet": "AI systems are transforming investment research by automating analysis and..."
    },
    {
      "document": "machine_learning_basics.txt",
      "score": 0.2104,
      "snippet": "Machine learning is a subset of artificial intelligence that enables systems..."
    },
    {
      "document": "deep_learning.txt",
      "score": 0.1893,
      "snippet": "Deep learning uses neural networks with many layers to learn complex..."
    }
  ]
}
```

---

#### `POST /index`

Rebuild the TF-IDF index. Use this after adding new `.txt` files to the `documents/` folder without restarting the server.

**Example:**

```bash
curl -X POST "http://localhost:8000/index"
```

**Response:**

```json
{
  "message": "Index rebuilt successfully"
}
```

---

#### `GET /`

Serves the search UI at `http://localhost:8000`.

---

#### `GET /docs`

FastAPI's auto-generated interactive API documentation (Swagger UI):

```
http://localhost:8000/docs
```

---

## Sample API Calls

```bash
# Search for AI topics
curl "http://localhost:8000/search?q=machine+learning+neural+networks"

# Search for finance topics
curl "http://localhost:8000/search?q=stock+market+investment+strategy"

# Search for health topics
curl "http://localhost:8000/search?q=cardiovascular+disease+prevention"

# Multi-word natural language query
curl "http://localhost:8000/search?q=how+does+deep+learning+work"

# Rebuild index after adding new documents
curl -X POST "http://localhost:8000/index"
```

---

## Constraints Compliance

| Requirement | Status | Details |
|---|---|---|
| No sklearn / gensim / spacy | ✅ | Zero NLP library dependencies |
| No Hugging Face / Transformers | ✅ | No pretrained embeddings used |
| Manual TF-IDF implementation | ✅ | `src/indexer.py` — fully hand-coded |
| Manual Cosine Similarity | ✅ | `src/searcher.py` — implemented from scratch |
| Only standard libraries | ✅ | Uses `math`, `re`, `os`, `collections`, `numpy` |
| Top 3 documents returned | ✅ | Configurable via `top_k` parameter |
| Similarity scores included | ✅ | Rounded to 4 decimal places |
| Text snippet (first 200 chars) | ✅ | `docs[idx][:200]` in `search()` |
| `POST /index` bonus endpoint | ✅ | Rebuilds index without server restart |
| Minimal UI | ✅ | `static/index.html` served at `/` |

---

## Dependencies

```
fastapi      — web framework
uvicorn      — ASGI server
pydantic     — response validation and serialization
numpy        — array operations for TF-IDF vectors
```

All text processing logic (tokenization, TF-IDF, cosine similarity) uses **only Python standard library**.
