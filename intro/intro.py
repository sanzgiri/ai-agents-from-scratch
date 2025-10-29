from llama_cpp import Llama
import os
from pathlib import Path

# Get the directory of the current file
current_dir = Path(__file__).parent

# Initialize and load the model
llama = Llama(
    model_path=str(current_dir / ".." / "models" / "Qwen3-1.7B-Q8_0.gguf"),
    n_ctx=2048,  # context size
    verbose=False
)

prompt = "do you know node-llama-cpp"

# Create chat completion
response = llama.create_chat_completion(
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# Extract and print the response
answer = response["choices"][0]["message"]["content"]
print(f"AI: {answer}")
