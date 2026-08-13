import streamlit as st

from modules.loader import load_documents
from modules.splitter import split_documents
from modules.vectorstore import (
    create_vectorstore,
    load_vectorstore
)
from modules.retriever import get_retriever
from modules.llm import get_llm
from modules.graph import build_graph


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Agentic AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic AI Knowledge Assistant")

st.caption(
    "Ask questions about the Agentic AI eBook. "
    "Answers are grounded in the provided document."
)


# =========================================================
# INITIALIZE RAG
# =========================================================

if "app" not in st.session_state:

    with st.spinner("Loading knowledge base..."):

        db = load_vectorstore()

        if db is None:

            documents = load_documents()

            chunks = split_documents(documents)

            db = create_vectorstore(chunks)

        retriever = get_retriever(db)

        llm = get_llm()

        st.session_state.app = build_graph(
            retriever,
            llm
        )


# =========================================================
# CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )

        if message["role"] == "assistant":

            # -----------------------------
            # Confidence
            # -----------------------------

            score = message.get(
                "score",
                0.0
            )

            st.caption(
                f"Retrieval confidence: {score:.2f}"
            )

            # -----------------------------
            # Retrieved Context
            # -----------------------------

            sources = message.get(
                "sources",
                []
            )

            if sources:

                with st.expander(
                    "📚 Retrieved Context"
                ):

                    for source in sources:

                        chunk_number = source.get(
                            "chunk",
                            0
                        )

                        page = source.get(
                            "page"
                        )

                        if page is not None:

                            page_number = page + 1

                            st.markdown(
                                f"### Chunk {chunk_number} — Page {page_number}"
                            )

                        else:

                            st.markdown(
                                f"### Chunk {chunk_number}"
                            )

                        st.write(
                            source["text"]
                        )

                        st.divider()


# =========================================================
# QUESTION
# =========================================================

question = st.chat_input(
    "Ask a question about the Agentic AI eBook..."
)


if question:

    # =====================================================
    # USER MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.write(question)


    # =====================================================
    # ASSISTANT
    # =====================================================

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching the document..."
        ):

            result = st.session_state.app.invoke(
                {
                    "question": question,
                    "context": "",
                    "reasoning": "",
                    "answer": "",
                    "sources": [],
                    "score": 0.0
                }
            )


        answer = result.get(
            "answer",
            "I don't know based on the provided document."
        )

        reasoning = result.get(
            "reasoning",
            ""
        )

        sources = result.get(
            "sources",
            []
        )

        score = result.get(
            "score",
            0.0
        )


        # =================================================
        # FINAL ANSWER
        # =================================================

        st.markdown("### Answer")

        st.write(answer)


        # =================================================
        # CONFIDENCE / SCORE
        # =================================================

        st.markdown(
            f"**Retrieval confidence:** `{score:.2f}`"
        )


        # =================================================
        # REASONING / EVIDENCE
        # =================================================

        if reasoning:

            with st.expander(
                "🧠 Why this answer?"
            ):

                st.write(reasoning)


        # =================================================
        # RETRIEVED CONTEXT
        # =================================================

        if sources:

            with st.expander(
                "📚 Retrieved Context"
            ):

                for source in sources:

                    chunk_number = source.get(
                        "chunk",
                        0
                    )

                    page = source.get(
                        "page"
                    )

                    if page is not None:

                        st.markdown(
                            f"### Chunk {chunk_number} — Page {page + 1}"
                        )

                    else:

                        st.markdown(
                            f"### Chunk {chunk_number}"
                        )

                    st.write(
                        source["text"]
                    )

                    st.divider()


    # =====================================================
    # SAVE MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "reasoning": reasoning,
            "sources": sources,
            "score": score
        }
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("About")

    st.write(
        "This chatbot answers questions strictly "
        "from the Agentic AI eBook."
    )

    st.write(
        "Each response provides the final answer, "
        "retrieved document chunks, and retrieval score."
    )

    st.write(
        "If the required information is not found "
        "in the document, the chatbot will not guess."
    )

    if st.button("Clear Chat"):

        st.session_state.messages = []

        st.rerun()