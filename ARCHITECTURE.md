# Arhitektura RAG Chatbota

## 📊 Tok podataka

```
┌──────────────────────────────────────────────────────────────┐
│                        SETUP FAZA (jednom)                   │
└──────────────────────────────────────────────────────────────┘

PDFs (./pdfs/)
    │
    ▼
┌─────────────┐
│  setup.py   │  1. Učitaj PDFove
│             │  2. Chunk na dijelove (1000 chars, overlap 200)
│             │  3. Multilingual embeddings (Sentence Transformers)
│             │  4. Spremi u ChromaDB
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ ChromaDB    │  Vektorska baza s embedding vektorima
│ ./chroma_db │  + metadata (filename, page)
└─────────────┘


┌──────────────────────────────────────────────────────────────┐
│                     QUERY FAZA (runtime)                     │
└──────────────────────────────────────────────────────────────┘

User pitanje
    │
    ▼
┌──────────────┐
│ rag_model.py │  1. Embedding pitanja (Sentence Transformers)
│              │  2. Similarity search (ChromaDB, top_k=3)
│              │  3. Sastavi kontekst
│              │  4. Prompt + kontekst → Gemini
│              │  5. Vrati odgovor + izvore
└──────┬───────┘
       │
       ├────────────────────┐
       │                    │
       ▼                    ▼
┌─────────────┐      ┌─────────────┐
│   api.py    │      │   app.py    │
│             │      │             │
│ POST /chat  │      │  Streamlit  │
│ (FastAPI)   │      │     UI      │
└─────────────┘      └─────────────┘
```

## 🗂️ 4 Glavne Komponente

### 1. setup.py
- **Uloga**: Priprema podatke (run jednom ili pri promjeni PDFova)
- **Input**: PDF datoteke iz `./pdfs/`
- **Output**: Popunjena ChromaDB baza
- **Koristi**: pypdf, sentence-transformers, chromadb

### 2. rag_model.py
- **Uloga**: Srce RAG logike
- **Metoda**: `respond(user_query) → {response, sources}`
- **Proces**:
  1. Embedduje upit (Sentence Transformers)
  2. Traži slične chunk-ove (ChromaDB)
  3. Sastavlja prompt s kontekstom
  4. Generira odgovor (Gemini)
- **Koristi**: sentence-transformers, google-generativeai, chromadb

### 3. api.py
- **Uloga**: REST API sučelje
- **Endpoint**: `POST /chat`
- **Request body**: `{"prompt": "pitanje", "top_k": 3}`
- **Response**: `{"response": "odgovor", "sources": [...]}`
- **Koristi**: fastapi, uvicorn, rag_model

### 4. app.py
- **Uloga**: Web UI za razgovor
- **Featuri**:
  - Chat interface s poviješću
  - Prikaz izvora
  - Primjeri pitanja
  - Brisanje razgovora
- **Koristi**: streamlit, rag_model

## 🔑 Ključne tehnologije

| Tehnologija | Svrha |
|-------------|-------|
| **Sentence Transformers** | Multilingvalni embeddings (50+ jezika) |
| **Gemini API** | Generiranje odgovora (LLM) |
| **ChromaDB** | Vektorska baza za similarity search |
| **pypdf** | Ekstrakcija teksta iz PDFova |
| **FastAPI** | REST API server |
| **Streamlit** | Web UI |

## 💾 Podaci

### Metadata u svakom chunku:
```python
{
    "text": "Chunk teksta...",
    "filename": "company_info.pdf",
    "page": 1
}
```

### Odgovor od RAG modela:
```python
{
    "response": "Odgovor generiran od Geminija...",
    "sources": [
        {"filename": "company_info.pdf", "page": 1},
        {"filename": "products_services.pdf", "page": 1}
    ]
}
```

## 🚀 Workflow

### Inicijalizacija (jednom):
```bash
pip install -r requirements.txt
cp .env.example .env
# Uredi .env - dodaj GEMINI_API_KEY
python setup.py
```

### Korištenje:
```bash
# Opcija A - Streamlit
streamlit run app.py

# Opcija B - API
python api.py
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Koja je adresa tvrtke?"}'
```
