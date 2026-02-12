# RAG Chatbot - Poslovni Asistent

RAG (Retrieval-Augmented Generation) chatbot template koji koristi Google Gemini za inteligentno odgovaranje na pitanja iz PDF dokumenata na hrvatskom jeziku.

## 📋 Funkcionalnosti

- ✅ Učitavanje lokalnih PDF dokumenata
- ✅ Ekstrakcija teksta iz PDF-ova
- ✅ Automatsko dijeljenje teksta u chunk-ove s preklapanjem
- ✅ Generiranje embedding vektora pomoću Gemini API-ja
- ✅ Spremanje u ChromaDB vektorsku bazu
- ✅ REST API chat endpoint za postavljanje pitanja
- ✅ Dohvaćanje najrelevantnijih chunk-ova na osnovu upita
- ✅ Generiranje odgovora s kontekstom pomoću Gemini-ja
- ✅ Vraćanje strukturiranog odgovora s popisom izvora (PDF + stranica)
- ✅ Potpuna podrška za hrvatski jezik

## 🚀 Brzo pokretanje

### 1. Instalacija ovisnosti

```bash
pip install -r requirements.txt
```

### 2. Konfiguracija

Kopirajte `.env.example` u `.env` i postavite svoj Gemini API ključ:

```bash
cp .env.example .env
```

Uredite `.env` datoteku:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Kako dobiti Gemini API ključ:**
1. Posjetite [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Prijavite se s Google računom
3. Generirajte novi API ključ
4. Kopirajte ključ u `.env` datoteku

### 3. Dodajte PDF dokumente

Stavite svoje PDF dokumente u `pdfs/` direktorij:

```bash
mkdir -p pdfs
# Kopirajte svoje PDF dokumente u pdfs/ direktorij
```

### 4. Indeksirajte dokumente

```bash
python indexer.py
```

### 5. Pokrenite server

```bash
python main.py
```

Ili s uvicornom:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server će biti dostupan na: http://localhost:8000

## 📖 Korištenje API-ja

### Swagger UI dokumentacija

Otvorite http://localhost:8000/docs za interaktivnu API dokumentaciju.

### Osnovni primjeri

#### 1. Provjera statusa

```bash
curl http://localhost:8000/status
```

#### 2. Indeksiranje dokumenata

```bash
curl -X POST http://localhost:8000/index \
  -H "Content-Type: application/json" \
  -d '{"clear_existing": true}'
```

#### 3. Postavljanje pitanja

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Koja je tema ovog dokumenta?",
    "top_k": 3
  }'
```

Odgovor:

```json
{
  "response": "Odgovor chatbota na hrvatskom jeziku...",
  "sources": [
    {
      "chunk_id": 1,
      "filename": "company_info.pdf",
      "page_number": 1
    },
    {
      "chunk_id": 2,
      "filename": "products_services.pdf",
      "page_number": 1
    }
  ]
}
```

### Testiranje s primjer dokumentima

Repozitorij uključuje 3 primjera PDF dokumenata u `pdfs/` direktoriju:
- `company_info.pdf` - Informacije o tvrtki
- `products_services.pdf` - Proizvodi i usluge
- `policies.pdf` - Pravila i politike

Možete testirati sustav s primjerima pitanja:

```bash
# Pitanje o tvrtki
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Koja je adresa tvrtke?"}'

# Pitanje o proizvodima
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Koliko košta ERP sustav?"}'

# Pitanje o politikama
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Koliko dana godišnjeg odmora imaju zaposlenici?"}'
```

## 🔧 Konfiguracija

Sve postavke se mogu prilagoditi putem `.env` datoteke:

| Parametar | Opis | Zadana vrijednost |
|-----------|------|-------------------|
| `GEMINI_API_KEY` | Google Gemini API ključ | - |
| `GEMINI_MODEL` | Gemini model za generiranje odgovora | `gemini-1.5-flash` |
| `GEMINI_EMBEDDING_MODEL` | Gemini model za embeddings | `models/text-embedding-004` |
| `CHROMA_DB_PATH` | Putanja do ChromaDB baze | `./chroma_db` |
| `PDF_FOLDER_PATH` | Putanja do PDF dokumenata | `./pdfs` |
| `CHUNK_SIZE` | Veličina chunka u znakovima | `1000` |
| `CHUNK_OVERLAP` | Preklapanje između chunkova | `200` |
| `TOP_K` | Broj chunk-ova za dohvaćanje | `3` |

### Dostupni Gemini modeli

**Za generiranje odgovora (GEMINI_MODEL):**
- `gemini-1.5-flash` - Brži, ekonomičniji model (preporučeno)
- `gemini-1.5-pro` - Snažniji model za kompleksnije zadatke
- `gemini-1.0-pro` - Starija verzija

**Za embeddings (GEMINI_EMBEDDING_MODEL):**
- `models/text-embedding-004` - Najnoviji embedding model (768 dimenzija) - preporučeno
- `models/embedding-001` - Stariji model

## 🏗️ Arhitektura

```
┌─────────────┐
│   PDF-ovi   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   PDF Loader    │  ← Učitava PDF-ove i ekstraktira tekst
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Text Chunker   │  ← Dijeli tekst u chunk-ove
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   Embeddings    │  ← Gemini API (text-embedding-004)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Vector DB      │  ← ChromaDB (cosine similarity)
│  (ChromaDB)     │
└──────┬──────────┘
       │
       │  Korisničko pitanje
       ▼
┌─────────────────┐
│  RAG Chatbot    │  ← Dohvaća kontekst + Gemini generira odgovor
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Chat Endpoint  │  ← FastAPI REST API
└─────────────────┘
```

## 📁 Struktura projekta

```
ChatbotPoslovna/
├── main.py              # FastAPI aplikacija i endpointi
├── chatbot.py           # RAG chatbot logika
├── indexer.py           # Indeksiranje dokumenata
├── pdf_loader.py        # Učitavanje PDF-ova
├── text_chunker.py      # Dijeljenje teksta u chunk-ove
├── embeddings.py        # Generiranje embedding vektora
├── vector_db.py         # ChromaDB operacije
├── config.py            # Konfiguracija
├── requirements.txt     # Python ovisnosti
├── .env.example         # Primjer konfiguracije
├── pdfs/                # Direktorij za PDF dokumente
└── chroma_db/           # ChromaDB baza (generira se automatski)
```

## 🛠️ Razvoj

### Testiranje u Pythonu

```python
from chatbot import RAGChatbot

# Inicijalizacija chatbota
chatbot = RAGChatbot()

# Postavi pitanje
result = chatbot.chat("Što je navedeno o...?", top_k=3)

print(result["response"])
for source in result["sources"]:
    print(f"Izvor: {source['filename']}, stranica {source['page_number']}")
```

### Ponovno indeksiranje

Za ponovno indeksiranje dokumenata s brisanjem postojećih:

```python
from indexer import DocumentIndexer

indexer = DocumentIndexer()
indexer.index_documents(clear_existing=True)
```

## 📝 Napomene

- **Gemini API limiti**: Besplatna razina ima ograničenja zahtjeva po minuti
- **Embedding model**: Koristi se `text-embedding-004` (768 dimenzija)
- **LLM model**: Koristi se `gemini-1.5-flash` za generiranje odgovora
- **Vektorska baza**: ChromaDB s cosine similarity
- **Jezik**: Odgovori su optimizirani za hrvatski jezik

## 🤝 Doprinos

Slobodno prijavite bugove ili predložite nova poboljšanja!

## 📄 Licenca

MIT License