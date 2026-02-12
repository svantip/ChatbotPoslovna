# Embedding Model Change Summary

## What Changed

Replaced Gemini text-embedding-004 with Sentence Transformers multilingual model for embeddings.

## Flow (As Required)

```
Parsing → chunking → embedding (multilingual model) → db
user prompt → embedding → similarity search on db → context → gemini → response
```

## Technical Changes

### 1. Dependencies (requirements.txt)
**Added:**
- `sentence-transformers==3.0.1`

**Purpose:**
- Multilingual embedding model library

### 2. Configuration (.env.example)
**Added:**
```env
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

**Options:**
- `paraphrase-multilingual-MiniLM-L12-v2` (default - faster, 384 dims)
- `paraphrase-multilingual-mpnet-base-v2` (alternative - larger, 768 dims)

### 3. Setup Script (setup.py)
**Before:**
```python
import google.generativeai as genai
# ... 
result = genai.embed_content(
    model="models/text-embedding-004",
    content=text
)
```

**After:**
```python
from sentence_transformers import SentenceTransformer
# ...
embedding_model = SentenceTransformer(EMBEDDING_MODEL)
embeddings = embedding_model.encode(texts, show_progress_bar=True)
```

### 4. RAG Model (rag_model.py)
**Before:**
```python
query_embedding = genai.embed_content(
    model="models/text-embedding-004",
    content=user_query
)['embedding']
```

**After:**
```python
self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
# ...
query_embedding = self.embedding_model.encode(user_query).tolist()
```

## Benefits

### 1. Cost Reduction
- ❌ Before: API calls for EVERY embedding (indexing + queries)
- ✅ After: Only API calls for LLM responses

### 2. Multilingual Support
- Supports 50+ languages including Croatian
- Optimized for semantic similarity across languages

### 3. Local Processing
- Embeddings generated locally (no internet required)
- Faster processing (no network latency)
- Privacy (data doesn't leave your machine)

### 4. Consistency
- Same model used for both document and query embeddings
- Better semantic matching

## Architecture

### Before:
```
PDFs → Chunk → Gemini API (embeddings) → ChromaDB
Query → Gemini API (embedding) → Search → Gemini API (LLM) → Response
```
**API Calls:** 3 per query (1 embedding + 1 search + 1 LLM)

### After:
```
PDFs → Chunk → Sentence Transformers (local) → ChromaDB
Query → Sentence Transformers (local) → Search → Gemini API (LLM) → Response
```
**API Calls:** 1 per query (only LLM)

## Usage

### Indexing (No API Key Needed for Embeddings)
```bash
# Only GEMINI_API_KEY needed for LLM responses
# Embeddings work without any API key
python setup.py
```

### Querying
```python
from rag_model import RAGModel

rag = RAGModel()  # Loads local embedding model
result = rag.respond("Pitanje?")  # Uses local model + Gemini for response
```

## Performance

### Embedding Model Specs:
- **Model:** paraphrase-multilingual-MiniLM-L12-v2
- **Size:** ~470 MB (downloaded once, cached locally)
- **Dimensions:** 384
- **Languages:** 50+ (including Croatian, English, German, French, etc.)
- **Speed:** ~1000 sentences/sec on CPU

### Comparison:
| Aspect | Gemini Embeddings | Sentence Transformers |
|--------|-------------------|----------------------|
| API Calls | Yes | No |
| Cost | Pay per use | Free |
| Speed | Network latency | Local (fast) |
| Dimensions | 768 | 384 |
| Privacy | Data sent to Google | Fully local |
| Internet | Required | Not required |

## Migration Notes

If you have an existing database with Gemini embeddings:
1. Delete `chroma_db/` directory
2. Run `python setup.py` to re-index with new embeddings
3. Dimension mismatch will prevent mixing old and new embeddings

## Verification

✅ Code review completed (2 minor issues fixed)
✅ Security scan passed (0 vulnerabilities)
✅ Documentation updated (README, ARCHITECTURE, QUICKSTART, SUMMARY)
✅ All files committed and pushed
