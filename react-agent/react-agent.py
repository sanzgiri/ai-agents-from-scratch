from llama_cpp import Llama
from pathlib import Path
import json
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from helper.prompt_debugger import PromptDebugger

# Get the directory of the current file
current_dir = Path(__file__).parent

# Initialize and load the model
llama = Llama(
    model_path=str(current_dir / ".." / "models" / "hf_giladgd_gpt-oss-20b.MXFP4.gguf"),
    n_ctx=2000,
    verbose=False
)

# ReAct-style system prompt for mathematical reasoning
system_prompt = """You are a mathematical assistant that uses the ReAct (Reasoning + Acting) approach.

CRITICAL: You must follow this EXACT pattern for every problem:

Thought: [Explain what calculation you need to do next and why]
Action: [Call ONE tool with specific numbers]
Observation: [Wait for the tool result]
Thought: [Analyze the result and decide next step]
Action: [Call another tool if needed]
Observation: [Wait for the tool result]
... (repeat as many times as needed)
Thought: [Once you have ALL the information needed to answer the question]
Answer: [Give the final answer and STOP]

RULES:
1. Only write "Answer:" when you have the complete final answer to the user's question
2. After writing "Answer:", DO NOT continue calculating or thinking
3. Break complex problems into the smallest possible steps
4. Use tools for ALL calculations - never calculate in your head
5. Each Action should call exactly ONE tool

EXAMPLE:
User: "What is 5 + 3, then multiply that by 2?"

Thought: First I need to add 5 and 3
Action: add(5, 3)
Observation: 8
Thought: Now I need to multiply that result by 2
Action: multiply(8, 2)
Observation: 16
Thought: I now have the final result
Answer: 16"""


# Simple calculator tools
def add(a: float, b: float) -> str:
    """Add two numbers together"""
    result = a + b
    print(f"\n   🔧 TOOL CALLED: add({a}, {b})")
    print(f"   📊 RESULT: {result}\n")
    return str(result)


def multiply(a: float, b: float) -> str:
    """Multiply two numbers together"""
    result = a * b
    print(f"\n   🔧 TOOL CALLED: multiply({a}, {b})")
    print(f"   📊 RESULT: {result}\n")
    return str(result)


def subtract(a: float, b: float) -> str:
    """Subtract second number from first number"""
    result = a - b
    print(f"\n   🔧 TOOL CALLED: subtract({a}, {b})")
    print(f"   📊 RESULT: {result}\n")
    return str(result)


def divide(a: float, b: float) -> str:
    """Divide first number by second number"""
    if b == 0:
        print(f"\n   🔧 TOOL CALLED: divide({a}, {b})")
        print(f"   ❌ ERROR: Division by zero\n")
        return "Error: Cannot divide by zero"
    result = a / b
    print(f"\n   🔧 TOOL CALLED: divide({a}, {b})")
    print(f"   📊 RESULT: {result}\n")
    return str(result)


# Function definitions for the model
functions = [
    {
        "name": "add",
        "description": "Add two numbers together",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "multiply",
        "description": "Multiply two numbers together",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "subtract",
        "description": "Subtract second number from first number",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "Number to subtract from"},
                "b": {"type": "number", "description": "Number to subtract"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "divide",
        "description": "Divide first number by second number",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "Dividend (number to be divided)"},
                "b": {"type": "number", "description": "Divisor (number to divide by)"}
            },
            "required": ["a", "b"]
        }
    }
]


def execute_function_call(function_name: str, arguments: dict) -> str:
    """Execute a function call based on the function name"""
    func_map = {
        "add": add,
        "multiply": multiply,
        "subtract": subtract,
        "divide": divide
    }
    
    if function_name in func_map:
        return func_map[function_name](arguments["a"], arguments["b"])
    else:
        return f"Error: Unknown function {function_name}"


def react_agent(user_prompt: str, max_iterations: int = 10) -> str:
    """ReAct Agent execution loop with proper output handling"""
    print("\n" + "=" * 70)
    print(f"USER QUESTION: {user_prompt}")
    print("=" * 70 + "\n")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    iteration = 0
    full_response = ""
    
    while iteration < max_iterations:
        iteration += 1
        print(f"--- Iteration {iteration} ---")
        
        # Get response from model
        response = llama.create_chat_completion(
            messages=messages,
            tools=functions,
            tool_choice="auto",
            max_tokens=300,
            stream=True
        )
        
        # Collect streaming response
        current_chunk = ""
        for chunk in response:
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta and delta["content"]:
                    content = delta["content"]
                    print(content, end="", flush=True)
                    current_chunk += content
        
        print()  # New line after streaming
        
        full_response += current_chunk
        
        # Add assistant message
        messages.append({"role": "assistant", "content": current_chunk})
        
        # Check if we have a final answer
        if "answer:" in current_chunk.lower():
            print("\n" + "=" * 70)
            print("FINAL ANSWER REACHED")
            print("=" * 70)
            return full_response
        
        # Check if model wants to call functions (re-query without streaming to get tool calls)
        check_response = llama.create_chat_completion(
            messages=messages,
            tools=functions,
            tool_choice="auto",
            max_tokens=1
        )
        
        check_message = check_response["choices"][0]["message"]
        
        if "tool_calls" in check_message and check_message["tool_calls"]:
            # Update the last message with tool calls
            messages[-1] = check_message
            
            # Execute tool calls
            for tool_call in check_message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"]) if tool_call["function"]["arguments"] else {}
                
                # Execute the function
                function_response = execute_function_call(function_name, function_args)
                
                # Add function response to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": function_response
                })
        else:
            # No tool calls, prompt for continuation
            messages.append({
                "role": "user",
                "content": "Continue your reasoning. What's the next step?"
            })
    
    print("\n⚠️  Max iterations reached without final answer")
    return full_response or "Could not complete reasoning within iteration limit."


# Test queries that require multi-step reasoning
queries = [
    "A store sells 15 items on Monday at $8 each, 20 items on Tuesday at $8 each, and 10 items on Wednesday at $8 each. What's the average number of items sold per day, and what's the total revenue?",
]

for query in queries:
    react_agent(query, max_iterations=15)
    print("\n")

# Debug
prompt_debugger = PromptDebugger({
    'outputDir': './logs',
    'filename': 'react_calculator.txt',
    'includeTimestamp': True,
    'appendMode': False
})

# Note: This will log the final state of messages
# prompt_debugger.debug({
#     'messages': messages,
#     'functions': functions
# })
