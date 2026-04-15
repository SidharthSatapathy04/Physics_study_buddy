"""
Streamlit UI for Physics Study Buddy
All expensive resources in @st.cache_resource
Dark-themed, student-friendly interface
"""

import streamlit as st
import uuid
import os
from datetime import datetime
import dotenv

# Load environment
dotenv.load_dotenv()

# Ensure GROQ_API_KEY is set
if not os.getenv("GROQ_API_KEY"):
    st.error("❌ GROQ_API_KEY not found in .env file. Please set it before running.")
    st.stop()


@st.cache_resource
def load_agent():
    """
    Load LLM, embedder, ChromaDB, and compiled graph.
    This runs once and caches all expensive resources.
    """
    from graph import initialize_resources, get_graph
    from langchain_groq import ChatGroq
    from sentence_transformers import SentenceTransformer
    import chromadb
    from knowledge_base import DOCUMENTS
    
    # Initialize resources
    llm, embedder, collection = initialize_resources()
    
    # Get compiled graph
    app = get_graph(llm, embedder, collection)
    
    return {
        "llm": llm,
        "embedder": embedder,
        "collection": collection,
        "graph": app,
        "documents": DOCUMENTS
    }


def initialize_session():
    """Initialize session state on page load."""
    if "messages_ui" not in st.session_state:
        st.session_state.messages_ui = []
    
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    
    if "meta_log" not in st.session_state:
        st.session_state.meta_log = []


def reset_conversation():
    """Reset conversation for new session."""
    st.session_state.messages_ui = []
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.meta_log = []
    st.rerun()


def format_message_bubble(role: str, content: str, sources: list = None, 
                         route: str = None, faithfulness: float = None) -> str:
    """Format a chat message as HTML/CSS bubble."""
    if role == "user":
        return f"""
        <div style='margin: 10px 0; display: flex; justify-content: flex-end;'>
            <div style='background: rgba(0,150,255,0.7); color: white; padding: 12px 16px; 
                        border-radius: 16px; max-width: 70%; word-wrap: break-word;'>
                {content}
            </div>
        </div>
        """
    else:  # assistant
        meta_html = ""
        if sources or route or faithfulness is not None:
            meta_html = "<div style='margin-top: 8px; font-size: 0.85em; color: #888;'>"
            if route:
                meta_html += f"🔀 Route: {route} | "
            if faithfulness is not None:
                meta_html += f"📊 Faithfulness: {faithfulness:.2f}"
            meta_html += "</div>"
        
        sources_html = ""
        if sources:
            sources_html = f"<div style='margin-top: 8px; display: flex; gap: 6px; flex-wrap: wrap;'>"
            for source in sources:
                sources_html += f"<span style='background: rgba(100,200,100,0.3); padding: 4px 8px; border-radius: 12px; font-size: 0.9em;'>📚 {source}</span>"
            sources_html += "</div>"
        
        return f"""
        <div style='margin: 10px 0; display: flex; justify-content: flex-start;'>
            <div style='background: rgba(50,50,50,0.8); color: white; padding: 12px 16px;
                        border-radius: 16px; max-width: 70%; word-wrap: break-word; border-left: 3px solid #00aa00;'>
                {content}
                {sources_html}
                {meta_html}
            </div>
        </div>
        """


def main():
    """Main Streamlit app."""
    st.set_page_config(page_title="Physics Study Buddy", layout="wide", initial_sidebar_state="expanded")
    
    # Dark theme CSS
    st.markdown("""
    <style>
        body {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        .stChatMessage {
            background: rgba(30, 30, 30, 0.9);
        }
        .stChatInputContainer {
            background: rgba(40, 40, 40, 0.95);
        }
        h1, h2, h3 {
            color: #00d4ff;
        }
        .stButton > button {
            background: linear-gradient(135deg, #0099ff 0%, #0077dd 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #00bbff 0%, #0099dd 100%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    initialize_session()
    
    # Load agent (cached)
    agent = load_agent()
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.title("🔬 Physics Study Buddy")
        st.markdown("**AI Tutor for B.Tech Physics**")
        st.markdown("---")
        
        st.subheader("📚 Topics Covered")
        topics = [doc["topic"] for doc in agent["documents"]]
        for i, topic in enumerate(topics, 1):
            st.caption(f"{i}. {topic}")
        
        st.markdown("---")
        st.subheader("⚡ Quick Prompts")
        
        quick_prompts = [
            "Explain conservation of energy",
            "How do I solve projectile motion problems?",
            "What is Faraday's law of induction?",
            "Derive the lens maker's formula",
            "Explain photoelectric effect",
            "What is semi-conductor physics?"
        ]
        
        for prompt in quick_prompts:
            if st.button(f"💡 {prompt}", key=prompt, use_container_width=True):
                st.session_state.quick_prompt = prompt
        
        st.markdown("---")
        
        if st.button("🔄 New Conversation", use_container_width=True):
            reset_conversation()
        
        st.markdown("---")
        st.subheader("📊 Last Response Stats")
        if st.session_state.meta_log:
            last_meta = st.session_state.meta_log[-1]
            st.metric("Route", last_meta.get("route", "—"))
            st.metric("Faithfulness", f"{last_meta.get('faithfulness', 0.0):.2f}")
            st.caption(f"Sources: {', '.join(last_meta.get('sources', []))}")
        else:
            st.info("No responses yet. Ask your first question!")
    
    # ===== MAIN AREA =====
    st.markdown("# 🎓 Physics Study Buddy")
    st.markdown("*Your personal AI tutor for B.Tech Physics*")
    st.markdown("**Knowledge Base:** 12 topics | **Tool:** Physics Calculator | **Evaluation:** Faithfulness Scoring")
    st.markdown("---")
    
    # Chat history
    for i, msg in enumerate(st.session_state.messages_ui):
        role = msg["role"]
        content = msg["content"]
        sources = msg.get("sources", [])
        route = msg.get("route")
        faithfulness = msg.get("faithfulness")
        
        st.markdown(
            format_message_bubble(role, content, sources, route, faithfulness),
            unsafe_allow_html=True
        )
    
    # Chat input
    col1, col2 = st.columns([10, 1])
    
    with col1:
        user_input = st.chat_input(
            "Ask a physics question... (or type 'help' for guidance)",
            key="chat_input"
        )
    
    with col2:
        # Handle quick prompt
        if "quick_prompt" in st.session_state:
            user_input = st.session_state.pop("quick_prompt")
    
    if user_input:
        # Add user message to UI immediately
        st.session_state.messages_ui.append({
            "role": "user",
            "content": user_input
        })
        
        # Show thinking message
        with st.spinner("🤔 Thinking..."):
            from graph import ask
            
            try:
                # Call agent
                result = ask(
                    user_input,
                    st.session_state.thread_id,
                    agent["llm"],
                    agent["embedder"],
                    agent["collection"]
                )
                
                # Add assistant response
                st.session_state.messages_ui.append({
                    "role": "assistant",
                    "content": result.get("answer", "No response generated."),
                    "sources": result.get("sources", []),
                    "route": result.get("route"),
                    "faithfulness": result.get("faithfulness", 0.0)
                })
                
                # Log metadata
                st.session_state.meta_log.append({
                    "route": result.get("route"),
                    "sources": result.get("sources", []),
                    "faithfulness": result.get("faithfulness", 0.0),
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.messages_ui.append({
                    "role": "assistant",
                    "content": f"Sorry, something went wrong: {str(e)}"
                })
        
        st.rerun()


if __name__ == "__main__":
    main()
