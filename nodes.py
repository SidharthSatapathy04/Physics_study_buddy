"""
All 8 LangGraph node functions for Physics Study Buddy
Each node takes state: PhysicsState and returns dict with only modified fields
Test-ready: each function can be called directly with mock state
"""

import re
from typing import Optional
from state import PhysicsState, SLIDING_WINDOW, FAITHFULNESS_THRESHOLD, MAX_EVAL_RETRIES
from prompts import SYSTEM_PROMPT, ROUTER_PROMPT, EVAL_PROMPT


def memory_node(state: PhysicsState) -> dict:
    """
    Append user question to messages, extract student name, apply sliding window.
    
    Returns: {"messages": updated, "student_name": name_or_none}
    """
    # Append new user message
    messages = state.get("messages", []).copy()
    messages.append({"role": "user", "content": state["question"]})
    
    # Extract student name from "my name is" pattern (case-insensitive)
    student_name = state.get("student_name")
    question_lower = state["question"].lower()
    
    if "my name is" in question_lower and not student_name:
        # Extract word after "my name is" using regex
        match = re.search(r"my name is\s+([a-zA-Z]+)", state["question"], re.IGNORECASE)
        if match:
            student_name = match.group(1).capitalize()
    
    # Apply sliding window: keep only last SLIDING_WINDOW messages
    if len(messages) > SLIDING_WINDOW:
        messages = messages[-SLIDING_WINDOW:]
    
    return {"messages": messages, "student_name": student_name}


def router_node(state: PhysicsState, llm) -> dict:
    """
    Route question to retrieve (concepts), tool (calculations), or memory_only (chat).
    
    Returns: {"route": "retrieve" | "tool" | "memory_only"}
    """
    from langchain_core.messages import HumanMessage
    
    try:
        # Call LLM with router prompt
        response = llm.invoke([HumanMessage(content=ROUTER_PROMPT.format(question=state["question"]))])
        route = response.content.strip().lower().split()[0] if response.content else "retrieve"
        
        # Validate route
        if route not in ("retrieve", "tool", "memory_only"):
            route = "retrieve"
        
        return {"route": route}
    
    except Exception as e:
        # Silently default to retrieve on error
        return {"route": "retrieve"}


def retrieval_node(state: PhysicsState, embedder, collection) -> dict:
    """
    Embed question, query ChromaDB for top 3 results, format context.
    
    Returns: {"retrieved": context_string, "sources": [topics], "tool_result": ""}
    """
    try:
        # Embed question
        embedding = embedder.encode(state["question"], show_progress_bar=False)
        embedding_list = embedding.tolist()
        
        # Query ChromaDB
        results = collection.query(
            query_embeddings=[embedding_list],
            n_results=3,
            include=["documents", "metadatas"]
        )
        
        # Format context
        context_parts = []
        sources = []
        
        if results["documents"] and len(results["documents"]) > 0:
            for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
                topic = metadata.get("topic", "Unknown")
                sources.append(topic)
                context_parts.append(f"[Topic: {topic}]\n{doc}")
        
        retrieved_context = "\n\n".join(context_parts) if context_parts else ""
        
        return {"retrieved": retrieved_context, "sources": sources, "tool_result": ""}
    
    except Exception as e:
        # Silently handle retrieval error
        return {"retrieved": "", "sources": [], "tool_result": ""}


def skip_retrieval_node(state: PhysicsState) -> dict:
    """
    Explicit no-op for memory_only and tool paths.
    Returns empty context to prevent state leakage.
    
    Returns: {"retrieved": "", "sources": [], "tool_result": ""}
    """
    return {"retrieved": "", "sources": [], "tool_result": ""}


def tool_node(state: PhysicsState, llm) -> dict:
    """
    Extract math expression from question, calculate result using physics calculator.
    
    Returns: {"tool_result": result_string, "retrieved": "", "sources": ["Physics Calculator"]}
    """
    from tools import extract_expression, physics_calculator
    
    try:
        # Extract expression using LLM
        expression = extract_expression(state["question"], llm)
        
        if expression.upper() == "NONE" or not expression.strip():
            result = "No clear numerical expression found. Please provide specific numbers in your question (e.g., 'distance = 50 m, time = ?')"
        else:
            # Calculate using physics calculator (never raises exception)
            result = physics_calculator(expression)
        
        return {"tool_result": result, "retrieved": "", "sources": ["Physics Calculator"]}
    
    except Exception as e:
        return {"tool_result": f"Tool error: {str(e)}", "retrieved": "", "sources": ["Physics Calculator"]}


def answer_node(state: PhysicsState, llm) -> dict:
    """
    Generate final answer from LLM using context, tool result, and conversation history.
    
    Returns: {"answer": formatted_answer}
    """
    from langchain_core.messages import HumanMessage, SystemMessage
    
    try:
        # Build greeting with student name if available
        greeting = ""
        if state.get("student_name"):
            greeting = f"Hi {state['student_name']}! "
        
        # Build context block
        context_block = ""
        if state.get("retrieved"):
            context_block = f"KNOWLEDGE BASE CONTEXT:\n{state['retrieved']}\n\n"
        
        # Build calculator result block
        calc_block = ""
        if state.get("tool_result"):
            calc_block = f"CALCULATOR RESULT:\n{state['tool_result']}\n\n"
        
        # Build conversation history (last 6 messages)
        history_msgs = state.get("messages", [])[-6:] if state.get("messages") else []
        history_text = ""
        for msg in history_msgs[:-1]:  # Exclude current question
            role = msg.get("role", "").capitalize()
            content = msg.get("content", "")
            history_text += f"{role}: {content}\n"
        
        history_block = f"CONVERSATION HISTORY:\n{history_text}\n\n" if history_text else ""
        
        # Add retry note if applicable
        retry_note = ""
        if state.get("eval_retries", 0) > 0:
            retry_note = f"[RETRY ATTEMPT {state['eval_retries']}] Be more conservative. Quote context directly. Add nothing not in context.\n\n"
        
        # Build final system prompt
        system_message = SYSTEM_PROMPT.format(
            knowledge_base_context=state.get("retrieved", ""),
            calculator_result=state.get("tool_result", ""),
            conversation_history=history_text,
            student_question=state["question"]
        )
        
        # Call LLM
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=state["question"])
        ]
        response = llm.invoke(messages)
        answer_content = response.content.strip()
        
        # Combine greeting + answer
        final_answer = (greeting + answer_content) if greeting else answer_content
        
        return {"answer": final_answer}
    
    except Exception as e:
        # Silently handle answer generation error
        return {"answer": f"I encountered an error generating the answer: {str(e)}. Please try rephrasing your question."}


def eval_node(state: PhysicsState, llm) -> dict:
    """
    Evaluate faithfulness of answer to retrieved context.
    Skips eval if no context (tool or memory_only path).
    
    Returns: {"faithfulness": score (0.0-1.0), "eval_retries": count}
    """
    from langchain_core.messages import HumanMessage, SystemMessage
    
    eval_retries = state.get("eval_retries", 0) + 1
    retrieved = state.get("retrieved", "")
    answer = state.get("answer", "")
    
    # Skip evaluation if no retrieved context (tool or memory_only path)
    if not retrieved:
        return {"faithfulness": 1.0, "eval_retries": eval_retries}
    
    try:
        # Truncate context to first 1200 chars for eval
        context_truncated = retrieved[:1200]
        
        # Call LLM to evaluate faithfulness
        eval_prompt = EVAL_PROMPT.format(context=context_truncated, answer=answer)
        messages = [
            SystemMessage(content="You are a faithfulness evaluator. Reply with ONLY a number between 0.0 and 1.0."),
            HumanMessage(content=eval_prompt)
        ]
        response = llm.invoke(messages)
        
        # Parse response as float
        try:
            score = float(response.content.strip())
            score = max(0.0, min(1.0, score))  # Clamp to [0.0, 1.0]
        except (ValueError, AttributeError):
            print(f"⚠️ Could not parse faithfulness score: {response.content}")
            score = 0.75  # Default to middle value
        
        print(f"📊 Faithfulness: {score:.2f} | Attempt: {eval_retries}")
        
        return {"faithfulness": score, "eval_retries": eval_retries}
    
    except Exception as e:
        # Silently default faithfulness on error
        return {"faithfulness": 0.75, "eval_retries": eval_retries}


def save_node(state: PhysicsState) -> dict:
    """
    Append assistant answer to message history.
    
    Returns: {"messages": updated}
    """
    messages = state.get("messages", []).copy()
    messages.append({"role": "assistant", "content": state["answer"]})
    
    return {"messages": messages}


if __name__ == "__main__":
    print("✅ All node functions imported successfully")
    print("Nodes: memory, router, retrieval, skip_retrieval, tool, answer, eval, save")
