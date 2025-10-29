from llama_cpp import Llama
from pathlib import Path
import json
from datetime import datetime
import sys

# Add parent directory to path to import helper
sys.path.append(str(Path(__file__).parent.parent))
from helper.prompt_debugger import PromptDebugger

# Get the directory of the current file
current_dir = Path(__file__).parent

# Initialize and load the model
llama = Llama(
    model_path=str(current_dir / ".." / "models" / "Qwen3-1.7B-Q8_0.gguf"),
    n_ctx=2000,
    verbose=False
)

system_prompt = """You are a professional chronologist who standardizes time representations across different systems.
    
Always convert times from 12-hour format (e.g., "1:46:36 PM") to 24-hour format (e.g., "13:46") without seconds 
before returning them."""


# Define tool/function for getting current time
def get_current_time() -> str:
    """Get the current time"""
    return datetime.now().strftime("%I:%M:%S %p")


# Function definitions for the model (OpenAI format)
functions = [
    {
        "name": "get_current_time",
        "description": "Get the current time",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]


def execute_function_call(function_name: str, arguments: dict) -> str:
    """Execute a function call based on the function name"""
    if function_name == "get_current_time":
        return get_current_time()
    else:
        return f"Error: Unknown function {function_name}"


# Build messages
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What time is it right now?"}
]

# Create chat completion with function calling
response = llama.create_chat_completion(
    messages=messages,
    tools=functions,
    tool_choice="auto"
)

# Check if the model wants to call a function
message = response["choices"][0]["message"]

if "tool_calls" in message and message["tool_calls"]:
    # Extract function call
    tool_call = message["tool_calls"][0]
    function_name = tool_call["function"]["name"]
    function_args = json.loads(tool_call["function"]["arguments"]) if tool_call["function"]["arguments"] else {}
    
    print(f"Model wants to call function: {function_name}")
    
    # Execute the function
    function_response = execute_function_call(function_name, function_args)
    print(f"Function returned: {function_response}")
    
    # Add the function call and response to messages
    messages.append(message)
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
else:
    # Model responded without function call
    answer = message.get("content", "")

print(f"AI: {answer}")

# Debug the prompts
prompt_debugger = PromptDebugger({
    'outputDir': './logs',
    'filename': 'qwen_prompts.txt',
    'includeTimestamp': True,
    'appendMode': False
})

# Log the conversation
prompt_debugger.debug({
    'messages': messages,
    'functions': functions,
    'response': answer
})
