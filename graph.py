"""
LangGraph assembly for Physics Study Buddy agent
Full graph with router, retrieval, tool, evaluation, and retry logic
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer
import chromadb
import os
import dotenv

from state import PhysicsState, create_initial_state, FAITHFULNESS_THRESHOLD, MAX_EVAL_RETRIES
from knowledge_base import DOCUMENTS
from nodes import (
    memory_node, router_node, retrieval_node, skip_retrieval_node,
    tool_node, answer_node, eval_node, save_node
)

# Load environment
dotenv.load_dotenv()

# Lazy initialization (will be done in load_agent for Streamlit caching)
_llm = None
_embedder = None
_collection = None
_graph = None


def initialize_resources():
    """Initialize LLM, embedder, and ChromaDB collection (expensive, cache this)."""
    global _llm, _embedder, _collection
    
    if _llm is None:
        _llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.7,
            max_tokens=1024
        )
    
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    if _collection is None:
        # ChromaDB in-memory collection
        client = chromadb.EphemeralClient()
        _collection = client.get_or_create_collection(name="physics_kb")
        
        # Add documents to collection
        ids = []
        documents = []
        metadatas = []
        
        for doc in DOCUMENTS:
            ids.append(doc["id"])
            documents.append(doc["text"])
            metadatas.append({"topic": doc["topic"]})
        
        # Embed and add to collection
        embeddings = _embedder.encode(documents, show_progress_bar=False)
        embeddings_list = [emb.tolist() for emb in embeddings]
        
        _collection.add(
            ids=ids,
            embeddings=embeddings_list,
            documents=documents,
            metadatas=metadatas
        )
        print(f"✅ ChromaDB collection initialized with {len(DOCUMENTS)} documents")
    
    return _llm, _embedder, _collection


def route_decision(state: PhysicsState):
    """Conditional routing based on state["route"]."""
    route = state.get("route", "retrieve")
    if route == "tool":
        return "tool"
    elif route == "memory_only":
        return "skip"
    else:
        return "retrieve"


def eval_decision(state: PhysicsState):
    """Conditional routing at eval node based on faithfulness."""
    eval_retries = state.get("eval_retries", 0)
    faithfulness = state.get("faithfulness", 0.0)
    
    # If max retries reached, save regardless of score
    if eval_retries >= MAX_EVAL_RETRIES:
        return "save"
    
    # If faithfulness below threshold, retry answer
    if faithfulness < FAITHFULNESS_THRESHOLD:
        return "answer"
    
    # Otherwise save
    return "save"


def build_graph(llm, embedder, collection):
    """Build and compile the LangGraph."""
    graph_builder = StateGraph(PhysicsState)
    
    # Add nodes
    graph_builder.add_node("memory", lambda state: memory_node(state))
    graph_builder.add_node("router", lambda state: router_node(state, llm))
    graph_builder.add_node("retrieval", lambda state: retrieval_node(state, embedder, collection))
    graph_builder.add_node("skip_retrieval", skip_retrieval_node)
    graph_builder.add_node("tool", lambda state: tool_node(state, llm))
    graph_builder.add_node("answer", lambda state: answer_node(state, llm))
    graph_builder.add_node("eval", lambda state: eval_node(state, llm))
    graph_builder.add_node("save", save_node)
    
    # Add edges
    graph_builder.add_edge(START, "memory")
    graph_builder.add_edge("memory", "router")
    
    # Router decision
    graph_builder.add_conditional_edges(
        "router",
        route_decision,
        {
            "retrieve": "retrieval",
            "tool": "tool",
            "skip": "skip_retrieval"
        }
    )
    
    # All paths lead to answer
    graph_builder.add_edge("retrieval", "answer")
    graph_builder.add_edge("tool", "answer")
    graph_builder.add_edge("skip_retrieval", "answer")
    
    # Answer to eval
    graph_builder.add_edge("answer", "eval")
    
    # Eval decision
    graph_builder.add_conditional_edges(
        "eval",
        eval_decision,
        {
            "answer": "answer",  # Retry answer node
            "save": "save"
        }
    )
    
    # Save to end
    graph_builder.add_edge("save", END)
    
    # Compile
    app = graph_builder.compile(checkpointer=MemorySaver())
    print("✅ Graph compiled successfully")
    
    return app


def get_graph(llm=None, embedder=None, collection=None):
    """Get or create the compiled graph."""
    global _graph
    
    if _graph is None:
        if llm is None or embedder is None or collection is None:
            llm, embedder, collection = initialize_resources()
        _graph = build_graph(llm, embedder, collection)
    
    return _graph


def ask(question: str, thread_id: str, llm=None, embedder=None, collection=None) -> dict:
    """
    Ask the Physics Study Buddy a question.
    
    Args:
        question: Student's physics question
        thread_id: Unique session ID for memory
        llm: Optional LLM instance
        embedder: Optional embedder instance  
        collection: Optional ChromaDB collection
    
    Returns:
        dict with question, route, sources, faithfulness, answer
    """
    if llm is None or embedder is None or collection is None:
        llm, embedder, collection = initialize_resources()
    
    app = get_graph(llm, embedder, collection)
    
    # Create initial state
    initial_state = create_initial_state(question)
    
    # Invoke graph
    result = app.invoke(initial_state, config={"configurable": {"thread_id": thread_id}})
    
    # Format output
    return {
        "question": question,
        "route": result.get("route"),
        "sources": result.get("sources", []),
        "faithfulness": result.get("faithfulness", 0.0),
        "answer": result.get("answer", ""),
        "eval_retries": result.get("eval_retries", 0)
    }


if __name__ == "__main__":
    import uuid
    
    # Test graph initialization
    print("\n🔬 Physics Study Buddy - Graph Test")
    print("=" * 50)
    
    llm, embedder, collection = initialize_resources()
    app = get_graph(llm, embedder, collection)
    
    # Test question
    test_question = "Explain Newton's second law"
    thread_id = str(uuid.uuid4())
    
    print(f"\nQuestion: {test_question}")
    print("-" * 50)
    
    result = ask(test_question, thread_id, llm, embedder, collection)
    
    print(f"Route: {result['route']}")
    print(f"Sources: {result['sources']}")
    print(f"Faithfulness: {result['faithfulness']:.2f}")
    print(f"Answer: {result['answer'][:200]}...")
    print(f"\n✅ Graph test successful!")
