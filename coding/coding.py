from llama_cpp import Llama
from pathlib import Path

# Get the directory of the current file
current_dir = Path(__file__).parent

# Initialize and load the model
llama = Llama(
    model_path=str(current_dir / ".." / "models" / "hf_giladgd_gpt-oss-20b.MXFP4.gguf"),
    n_ctx=2048,
    verbose=False
)

q1 = "What is hoisting in JavaScript? Explain with examples."

print(f"Context size: {llama.n_ctx()}")

# Create streaming chat completion
response = llama.create_chat_completion(
    messages=[
        {"role": "user", "content": q1}
    ],
    max_tokens=2000,
    stream=True
)

# Stream the response
print("\nAI: ", end="", flush=True)
full_response = ""
for chunk in response:
    if "choices" in chunk and len(chunk["choices"]) > 0:
        delta = chunk["choices"][0].get("delta", {})
        if "content" in delta:
            content = delta["content"]
            print(content, end="", flush=True)
            full_response += content

print(f"\n\nFinal answer:\n {full_response}")
