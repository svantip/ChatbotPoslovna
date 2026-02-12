"""
RAG Model - Similarity search + Gemini response generation.
"""
import os
import chromadb
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
TOP_K = int(os.getenv("TOP_K", "3"))


class RAGModel:
    """RAG model for Croatian chatbot."""

    def __init__(self):
        """Initialize the RAG model."""
        # Initialize Gemini
        if not GEMINI_API_KEY:
            raise ValueError("❌ GEMINI_API_KEY is not set in .env file")

        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

        # Load embedding model (multilingual)
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

        # Initialize ChromaDB
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection = client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

        print(f"✓ RAG Model initialized")
        print(f"  - Gemini Model (response): {GEMINI_MODEL}")
        print(f"  - Embedding Model: {EMBEDDING_MODEL}")
        print(f"  - Documents in DB: {self.collection.count()}")

    def respond(self, user_query, top_k=None):
        """
        Generate response for user query using RAG.
        Returns: dict {response, sources}
        """
        if top_k is None:
            top_k = TOP_K

        top_k = max(4, min(int(top_k), 10))

        # Embedding upita
        query_embedding = self.embedding_model.encode(
            user_query, convert_to_numpy=True, normalize_embeddings=True
        ).tolist()

        # Similarity search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]

        if not docs:
            return {
                "response": "Nisam pronašao relevantne informacije u dokumentima.",
                "sources": []
            }

        # Context + izvori (dedupe)
        context_blocks = []
        sources = []
        seen = set()

        for i, (doc, meta, dist) in enumerate(zip(docs, metas, dists), start=1):
            filename = meta.get("filename", "Nepoznat dokument")
            page = meta.get("page", None)  # bolje None nego "Unknown"
            topic = meta.get("topic", "unknown")
            content_type = meta.get("content_type", "unknown")

            key = (filename, page) if page is not None else (filename, i)
            if key not in seen:
                seen.add(key)
                sources.append({
                    "filename": filename,
                    "page": page,
                    "topic": topic,
                    "content_type": content_type,
                    "distance": dist
                })

            context_blocks.append(
                f"[{i}] source={filename} page={page} topic={topic} type={content_type}\n{doc}"
            )

        context = "\n\n".join(context_blocks)

        legal_triggers = ["smijem", "dozvola", "dozvole", "legalno",
                          "zakonito", "mogu li", "trebam li", "kazna", "inspekcija"]
        is_legal = any(t in user_query.lower() for t in legal_triggers)

        prompt = f"""
    Ti si informativni chatbot za područje gradnje i arhitekture u Republici Hrvatskoj.

    PRAVILA:
    - Odgovaraj ISKLJUČIVO na temelju danog konteksta. Ne izmišljaj činjenice.
    - Ako informacija nije u kontekstu, reci: "U dostupnim dokumentima nemam taj podatak."
    - Ne spominji riječi "kontekst", "chunk", "embedding" ni kako sustav radi.
    - Ne daješ pravne savjete. Ako pitanje traži pravno tumačenje ili odluku, daj opću informaciju i dodaj napomenu da se za konkretan slučaj treba provjeriti službeni tekst ili konzultirati stručnjaka.

    FORMAT ODGOVORA:
    1) Kratki odgovor (2–5 rečenica)
    2) Objašnjenje ako je potrebno (ako je pitanje kompleksno ili pravno) - ne duže od 2-3 rečenice
    3) Preporučeni resursi (ako su linkovi u kontekstu)
    4) Napomena (samo ako je potrebno, npr. pravna tema)

    KONTEKST:
    {context}

    PITANJE:
    {user_query}

    Odgovori na standardnom hrvatskom jeziku.
    """

        try:
            response = self.model.generate_content(prompt)
            cleaned_sources = [
                {"filename": s["filename"], "page": s["page"]}
                for s in sources
            ]

            # Ako je pravno pitanje, a model slučajno nije dodao napomenu
            text = response.text.strip()
            if is_legal and "pravni savjet" not in text.lower():
                text += "\n\nNapomena: Ovo je informativan odgovor i ne predstavlja pravni savjet. Za konkretan slučaj provjerite službeni tekst propisa ili se obratite ovlaštenom stručnjaku."

            return {"response": text, "sources": cleaned_sources}

        except Exception as e:
            return {
                "response": f"Greška pri generiranju odgovora: {str(e)}",
                "sources": [{"filename": s["filename"], "page": s["page"]} for s in sources]
            }


if __name__ == "__main__":
    print("Testing RAG Model...")

    try:
        rag = RAGModel()

        test_query = "Koja je adresa tvrtke?"
        print(f"\nTest pitanje: {test_query}")

        result = rag.respond(test_query)

        print(f"\nOdgovor: {result['response']}")
        print(f"\nIzvori:")
        for source in result['sources']:
            print(f"  • {source['filename']}, stranica {source['page']}")

    except Exception as e:
        print(f"❌ Error: {e}")
