# RAG Chatbot - Poslovni Asistent

RAG (Retrieval-Augmented Generation) chatbot koji koristi Google Gemini za generiranje odgovora. Izuzetno jednostavna arhitektura s samo 4 skripta.

## 📋 Funkcionalnosti

- ✅ Učitavanje PDF dokumenata i ekstrakcija teksta
- ✅ Automatsko chunking s preklapanjem
- ✅ Gemini embeddings (text-embedding-004)
- ✅ ChromaDB vektorska baza
- ✅ Similarity search za pronalaženje relevantnog konteksta
- ✅ Gemini za generiranje odgovora na hrvatskom
- ✅ REST API endpoint
- ✅ Streamlit UI za chat
- ✅ Praćenje izvora (PDF + stranica)

## 🚀 Brzo pokretanje

### 1. Instalacija

```bash
pip install -r requirements.txt
```

### 2. Konfiguracija

```bash
cp .env.example .env
# Uredite .env i postavite GEMINI_API_KEY
```

### 3. Indeksiranje dokumenata

```bash
python setup.py
```

### 4. Pokrenite aplikaciju

**Opcija A - Streamlit UI:**
```bash
streamlit run app.py
```

**Opcija B - API server:**
```bash
python api.py
# ili
uvicorn api:app --reload
```

API dokumentacija: http://localhost:8000/docs

## 📖 Korištenje

### Streamlit UI

Najjednostavniji način - otvorite browser na http://localhost:8501 i chatajte!

### REST API

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Koja je adresa tvrtke?",
    "top_k": 3
  }'
```

Odgovor:
```json
{
  "response": "Adresa tvrtke je...",
  "sources": [
    {"filename": "company_info.pdf", "page": 1}
  ]
}
```

## 🔧 Konfiguracija (.env)

| Parametar | Opis | Default |
|-----------|------|---------|
| `GEMINI_API_KEY` | Google Gemini API ključ | - |
| `GEMINI_MODEL` | Gemini model | `gemini-1.5-flash` |
| `PDF_FOLDER_PATH` | Putanja do PDFova | `./pdfs` |
| `CHROMA_DB_PATH` | Putanja do DB | `./chroma_db` |
| `CHUNK_SIZE` | Veličina chunka | `1000` |
| `CHUNK_OVERLAP` | Preklapanje | `200` |
| `TOP_K` | Broj rezultata | `3` |

**Dobivanje API ključa:** https://makersuite.google.com/app/apikey

## 🔧 Struktura projekta

```
ChatbotPoslovna/
├── setup.py          # Script 1: Parse PDFs, chunk, embed, store
├── rag_model.py      # Script 2: RAG logic (similarity search + Gemini)
├── api.py            # Script 3: FastAPI REST endpoint
├── app.py            # Script 4: Streamlit UI
├── requirements.txt  # Dependencies
├── .env.example      # Environment template
├── pdfs/             # Your PDF documents (3 samples included)
└── chroma_db/        # Vector database (auto-generated)
```

## ⚙️ Kako radi

1. **setup.py** - Učitava PDFove, dijeli na chunkove, embeduje i sprema u ChromaDB
2. **rag_model.py** - Provodi similarity search i generira odgovore s Geminijem
3. **api.py** - Izlaže `respond()` funkciju preko POST `/chat` endpointa
4. **app.py** - Streamlit sučelje koje koristi RAGModel

## 🛠️ Razvoj

### Testiranje RAG modela

```python
from rag_model import RAGModel

rag = RAGModel()
result = rag.respond("Koja je adresa tvrtke?")
print(result["response"])
```

### Ponovno indeksiranje

```bash
python setup.py  # Automatski briše staru bazu i kreira novu
```

## 📝 Napomene

- **Gemini**: Koristi se za embeddings (text-embedding-004) i generiranje odgovora (gemini-1.5-flash)
- **Bez kompleksnosti**: Samo 4 skripta, jednostavna arhitektura
- **Hrvatski**: Odgovori optimizirani za hrvatski jezik
- **Primjeri**: 3 PDF dokumenta uključena (tvrtka, proizvodi, politike)

## 🤝 Doprinos

Slobodno prijavite bugove ili predložite poboljšanja!