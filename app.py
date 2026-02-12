"""
Script 4: Streamlit UI - User interface for the chatbot.
Run with: streamlit run app.py
"""
import streamlit as st
from rag_model import RAGModel

# Page config
st.set_page_config(
    page_title="Semantički savjetnik za projektiranje i gradnju",
    page_icon="🏗️",
    layout="centered"
)

# Initialize RAG model (with caching)


@st.cache_resource
def load_rag_model():
    """Load RAG model once and cache it."""
    try:
        return RAGModel()
    except Exception as e:
        st.error(f"❌ Failed to initialize RAG model: {e}")
        st.info(
            "Make sure to:\n1. Run `python setup.py` first\n2. Set GEMINI_API_KEY in .env file")
        return None


# Main UI
def main():
    st.title("🏗️ Semantički savjetnik za projektiranje i gradnju")
    st.markdown("Postavite pitanja o dokumentima na hrvatskom jeziku")

    # Load model
    rag_model = load_rag_model()

    if rag_model is None:
        st.stop()

    # Show database info
    doc_count = rag_model.collection.count()
    st.sidebar.success(f"✓ Inicijalizirano")
    st.sidebar.info(f"📚 Dokumenata u bazi: {doc_count}")

    # Chat interface
    st.markdown("---")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("📄 Izvori"):
                    for source in message["sources"]:
                        st.write(
                            f"• {source['filename']}, stranica {source['page']}")

    # Chat input
    if prompt := st.chat_input("Postavite pitanje..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Razmišljam..."):
                result = rag_model.respond(prompt)

            st.markdown(result["response"])

            if result["sources"]:
                with st.expander("📄 Izvori"):
                    for source in result["sources"]:
                        st.write(
                            f"• {source['filename']}, stranica {source['page']}")

        # Add assistant message to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "sources": result["sources"]
        })

    # Clear chat button
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑️ Obriši razgovor"):
        st.session_state.messages = []
        st.rerun()


if __name__ == "__main__":
    main()
