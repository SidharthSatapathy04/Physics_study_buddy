"""
PhysicsState TypedDict and constants for the Physics Study Buddy agent
"""

from typing import TypedDict, List, Optional

class PhysicsState(TypedDict):
    """
    Complete state for the Physics Study Buddy agent.
    Every field must be present — nodes will KeyError if missing.
    """
    question: str               # Current student question
    messages: List[dict]        # Full conversation history [{role, content}]
    route: str                  # 'retrieve' | 'tool' | 'memory_only'
    retrieved: str              # Formatted context string from ChromaDB
    sources: List[str]          # Topic names of retrieved documents
    tool_result: str            # String output from physics calculator
    answer: str                 # Final LLM-generated answer
    faithfulness: float         # Faithfulness score 0.0–1.0 from eval node
    eval_retries: int           # Number of answer retry attempts so far
    student_name: Optional[str] # Extracted student name if given


# Configuration constants
FAITHFULNESS_THRESHOLD = 0.7
MAX_EVAL_RETRIES = 2
SLIDING_WINDOW = 8  # Keep last 8 messages in history

# Initial state factory
def create_initial_state(question: str) -> PhysicsState:
    """Create a fresh initial state for a new question."""
    return {
        "question": question,
        "messages": [],
        "route": "",
        "retrieved": "",
        "sources": [],
        "tool_result": "",
        "answer": "",
        "faithfulness": 0.0,
        "eval_retries": 0,
        "student_name": None,
    }
