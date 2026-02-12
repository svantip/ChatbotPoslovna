# Brzi Početak / Quick Start Guide

## 🚀 Za nestrpljive

```bash
# 1. Instaliraj dependencies
pip install -r requirements.txt

# 2. Postavi API ključ
cp .env.example .env
# Uredi .env i dodaj GEMINI_API_KEY

# 3. Indeksiraj dokumente
python setup.py

# 4A. Pokreni Streamlit UI
streamlit run app.py

# ILI 4B. Pokreni API server
python api.py
```

## 📂 4 Skripta - To je to!

1. **setup.py** - Indeksiranje PDFova (jednom)
2. **rag_model.py** - RAG logika (similarity search + Gemini)
3. **api.py** - REST API (POST /chat)
4. **app.py** - Streamlit UI

## 📝 Testiranje

### Streamlit UI
```bash
streamlit run app.py
# Otvori http://localhost:8501
```

### API
```bash
# Terminal 1
python api.py

# Terminal 2
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Koja je adresa tvrtke?"}'
```

### Dokumentacija
```
http://localhost:8000/docs
```

## 🔑 Gemini API Ključ

1. https://makersuite.google.com/app/apikey
2. Create API Key
3. Kopiraj u .env

## 💡 Primjeri pitanja

- "Koja je adresa tvrtke?"
- "Koliko košta ERP sustav?"
- "Koliko dana godišnjeg odmora?"
- "Koje usluge nudi tvrtka?"

## 📦 Što je uključeno?

- 3 primjera PDF dokumenata
- ChromaDB za vektore
- Sentence Transformers za embeddings (multilingvalni)
- Gemini za generiranje odgovora
- API + Streamlit UI

## 🆘 Pomoć

Vidi README.md za detaljnije informacije.
