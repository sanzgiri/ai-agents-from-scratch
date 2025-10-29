from llama_cpp import Llama
from pathlib import Path
import json
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from memory_manager import MemoryManager

# Get the directory of the current file
current_dir = Path(__file__).parent

# Initialize memory manager
memory_manager = MemoryManager('./agent-memory.json')

# Load existing memories and add to system prompt
memory_summary = memory_manager.get_memory_summary()

system_prompt = f"""You are a helpful assistant with long-term memory.
{memory_summary}

When the user shares important information about themselves, their preferences, or facts 
they want you to remember, use the saveMemory function to store it."""

# Initialize and load the model
llama = Llama(
    model_path=str(current_dir / ".." / "models" / "Qwen3-1.7B-Q8_0.gguf"),
    n_ctx=2000,
    verbose=False
)


# Define memory saving function
def save_memory(memory_type: str, content: str, key: str = None) -> str:
    """Save important information to long-term memory"""
    if memory_type == "fact":
        memory_manager.add_fact(content)
        return "Fact saved to memory"
    elif memory_type == "preference":
        key = key or content.split()[0]
        memory_manager.add_preference(key, content)
        return "Preference saved to memory"
    return "Unknown memory type"


# Function definitions for the model
functions = [
    {
        "name": "save_memory",
        "description": "Save important information to long-term memory (user preferences, facts, personal details)",
        "parameters": {
            "type": "object",
            "properties": {
                "memory_type": {
                    "type": "string",
                    "enum": ["fact", "preference"],
                    "description": "Type of memory to save"
                },
                "content": {
                    "type": "string",
                    "description": "The information to remember"
                },
                "key": {
                    "type": "string",
                    "description": "For preferences: the preference key (e.g., 'favorite_color')"
                }
            },
            "required": ["memory_type", "content"]
        }
    }
]


def execute_function_call(function_name: str, arguments: dict) -> str:
    """Execute a function call based on the function name"""
    if function_name == "save_memory":
        return save_memory(
            memory_type=arguments.get("memory_type"),
            content=arguments.get("content"),
            key=arguments.get("key")
        )
    else:
        return f"Error: Unknown function {function_name}"


def chat(user_message: str, messages: list) -> str:
    """Send a message and get a response, handling function calls"""
    messages.append({"role": "user", "content": user_message})
    
    response = llama.create_chat_completion(
        messages=messages,
        tools=functions,
        tool_choice="auto"
    )
    
    message = response["choices"][0]["message"]
    
    # Check if the model wants to call a function
    if "tool_calls" in message and message["tool_calls"]:
        # Add assistant message with tool call
        messages.append(message)
        
        # Execute each tool call
        for tool_call in message["tool_calls"]:
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
        
        # Get final response from model
        final_response = llama.create_chat_completion(
            messages=messages,
            tools=functions
        )
        
        answer = final_response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": answer})
    else:
        # Model responded without function call
        answer = message.get("content", "")
        messages.append({"role": "assistant", "content": answer})
    
    return answer


# Example conversation
messages = [{"role": "system", "content": system_prompt}]

# First interaction
prompt1 = "Hi! My name is Alex and I love pizza."
response1 = chat(prompt1, messages)
print(f"User: {prompt1}")
print(f"AI: {response1}\n")

# Later conversation (even after restarting the script)
prompt2 = "What's my favorite food?"
response2 = chat(prompt2, messages)
print(f"User: {prompt2}")
print(f"AI: {response2}")
