from typing import TypedDict
from langgraph.graph import StateGraph, END
from modules.prompts import RAG_PROMPT


NO_ANSWER_MESSAGE = "I don't know based on the provided document."

class State(TypedDict):
    question: str
    context: str
    reasoning: str
    answer: str
    sources: list
    score: float


def build_graph(retriever, llm):
    def retrieve_node(state):
        question = state["question"]
        # Retrieve documents
        docs = retriever.invoke(question)
        # No documents retrieved
        if not docs:
            return {
                **state,
                "context": "",
                "reasoning": "No relevant document chunks were retrieved.",
                "answer": NO_ANSWER_MESSAGE,
                "sources": [],
                "score": 0.0,
            }

        # Build context
        context_parts = []
        for doc in docs:
            text = doc.page_content.strip()
            if text:
                context_parts.append(text)
        context = "\n\n".join(context_parts)

        # Get similarity scores
        score = 0.0
        try:
            scored_docs = retriever.vectorstore.similarity_search_with_score(
                question,
                k=len(docs)
            )
            if scored_docs:
                # Chroma distance:
                # lower distance = more similar
                distances = [
                    float(distance)
                    for _, distance in scored_docs
                ]
                best_distance = min(distances)
                # Convert distance into an easy-to-read
                # confidence-like score.
                score = max(0.0,
                    min(
                        1.0,
                        1.0 - best_distance
                    )
                )
        except Exception:
            score = 0.0

        # Store retrieved chunks
        sources = []
        for i, doc in enumerate(docs, start=1):
            metadata = doc.metadata or {}
            sources.append(
                {
                    "text": doc.page_content,
                    "page": metadata.get("page"),
                    "source": metadata.get("source"),
                    "chunk": i,
                }
            )

        return {
            **state,
            "context": context,
            "sources": sources,
            "score": score,
        }

    # Generate answer
    def generate_node(state):
        # No useful context
        if not state.get("context", "").strip():
            return {
                **state,
                "answer": NO_ANSWER_MESSAGE,
            }
        prompt = RAG_PROMPT.format(
            context=state["context"],
            question=state["question"],
        )

        response = llm.invoke(prompt)
        raw_text = response.content.strip()
        reasoning, answer = _parse_response(raw_text)

        # Safety check
        if not answer.strip():
            answer = NO_ANSWER_MESSAGE
        return {
            **state,
            "reasoning": reasoning,
            "answer": answer,
        }

    # Build LangGraph
    graph = StateGraph(State)
    graph.add_node("retrieve",retrieve_node)
    graph.add_node("generate",generate_node)
    graph.set_entry_point("retrieve")

    graph.add_edge("retrieve","generate")
    graph.add_edge("generate",END)

    return graph.compile()


def _parse_response(raw_text):
    reasoning = ""
    answer = raw_text.strip()
    if "Answer:" in raw_text:
        parts = raw_text.split(
            "Answer:",
            1
        )

        reasoning_part = parts[0]
        answer = parts[1].strip()
        if "Reasoning:" in reasoning_part:
            reasoning = reasoning_part.split(
                "Reasoning:",
                1
            )[1].strip()

        else:
            reasoning = reasoning_part.strip()
    return reasoning, answer