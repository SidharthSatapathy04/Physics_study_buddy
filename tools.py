"""
Safe Physics Calculator Tool
Never raises exceptions — always returns error strings.
Restricted namespace prevents arbitrary code execution.
"""

import math
from typing import Any

# Restricted namespace: only safe math functions
SAFE_NAMESPACE = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "pi": math.pi,
    "e": math.e,
    "abs": abs,
    "pow": pow,
    "ceil": math.ceil,
    "floor": math.floor,
}


def physics_calculator(expression: str) -> str:
    """
    Safe physics calculator using restricted eval.
    
    Args:
        expression: Python-evaluable math expression (e.g., "sqrt(2 * 9.8 * 10)")
    
    Returns:
        Formatted result string or error message (never raises exception)
    """
    try:
        # Strip whitespace
        expression = expression.strip()
        
        if not expression:
            return "Error: Empty expression provided. Please provide a valid mathematical expression."
        
        # Evaluate in restricted namespace
        result = eval(expression, {"__builtins__": {}}, SAFE_NAMESPACE)
        
        # Handle non-numeric results
        if not isinstance(result, (int, float, complex)):
            return f"Error: Expression resulted in non-numeric type {type(result).__name__}."
        
        # Format result with 6 significant figures
        if isinstance(result, complex):
            formatted = f"{result.real:.6g} + {result.imag:.6g}i"
        else:
            formatted = f"{result:.6g}"
        
        return f"Result: {formatted}"
    
    except ZeroDivisionError:
        return "Error: Division by zero — check your input values."
    
    except ValueError as e:
        return f"Error: Invalid value — {str(e)}. Check domain constraints (e.g., sqrt of negative, asin > 1)."
    
    except SyntaxError:
        return "Error: Invalid syntax in expression. Write expressions in Python syntax, e.g., sqrt(2 * 9.8 * 10) or (1/2) * 5 * 4**2"
    
    except NameError as e:
        return f"Error: Unknown function or variable — {str(e)}. Allowed: sqrt, sin, cos, tan, asin, acos, atan, log, log10, exp, pi, e, abs, pow, ceil, floor"
    
    except Exception as e:
        return f"Calculator error: {type(e).__name__}: {str(e)}. Write expressions in Python syntax, e.g., sqrt(2 * 9.8 * 10) or (1/2) * 5 * 4**2"


def extract_expression(question: str, llm) -> str:
    """
    Use LLM to extract Python-evaluable math expression from question.
    
    Args:
        question: Student's question
        llm: LangChain LLM instance (langchain_groq.ChatGroq)
    
    Returns:
        Python expression string or "NONE" if no calculation possible
    """
    from langchain_core.messages import HumanMessage, SystemMessage
    
    extraction_prompt = """You are a physics assistant. Extract ONLY the Python-evaluable mathematical expression from the student's question.

Rules:
1. Return ONLY the expression (no explanation, no units)
2. Use Python math syntax: sqrt(), sin(), cos(), etc.
3. Constants: pi, e
4. If the question contains a numerical calculation, extract it exactly as (expression)
5. If no clear numeric expression exists, return exactly: NONE

Examples:
Question: "If a ball falls 50 meters, what is the time taken? Use g = 9.8 m/s²"
Expression: sqrt(2 * 50 / 9.8)

Question: "Calculate the escape velocity from Earth (radius 6.371e6 m, mass 5.972e24 kg). G = 6.674e-11"
Expression: sqrt(2 * 6.674e-11 * 5.972e24 / 6.371e6)

Question: "What color is copper?"
Expression: NONE

Student question: {question}

Reply with ONLY the expression or NONE."""
    
    try:
        messages = [
            SystemMessage(content="You are a physicist extracting math expressions. Reply with ONLY the expression or NONE."),
            HumanMessage(content=extraction_prompt.format(question=question))
        ]
        response = llm.invoke(messages)
        expression = response.content.strip()
        return expression if expression else "NONE"
    
    except Exception as e:
        return "NONE"


if __name__ == "__main__":
    # Test physics calculator
    print("Testing Physics Calculator:")
    print(f"sqrt(9) = {physics_calculator('sqrt(9)')}")
    print(f"sin(pi/2) = {physics_calculator('sin(pi/2)')}")
    print(f"(1/2) * 5 * 4**2 = {physics_calculator('(1/2) * 5 * 4**2')}")
    print(f"1/0 = {physics_calculator('1/0')}")
    print(f"__import__ = {physics_calculator('__import__')}")
    print("✅ All tests returned strings (no exceptions raised)")
