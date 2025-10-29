from llama_cpp import Llama
from pathlib import Path
import asyncio

"""
Asynchronous execution improves performance in GAIA benchmarks,
multi-agent applications, and other high-throughput scenarios.

Note: llama-cpp-python doesn't natively support multiple sequences like node-llama-cpp.
This example demonstrates parallel execution using asyncio and separate model instances
or by processing prompts in parallel batches.
"""

# Get the directory of the current file
current_dir = Path(__file__).parent
model_path = str(current_dir / ".." / "models" / "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf")


async def process_prompt(llama: Llama, prompt: str, label: str):
    """Process a single prompt asynchronously"""
    # In Python, we run the blocking call in an executor
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: llama.create_chat_completion(
            messages=[{"role": "user", "content": prompt}]
        )
    )
    answer = response["choices"][0]["message"]["content"]
    return label, prompt, answer


async def main():
    # Initialize the model (can be shared for sequential processing)
    # For true parallel processing, you'd need separate model instances or thread pooling
    llama = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_batch=1024,  # The number of tokens that can be processed at once
        verbose=False
    )

    q1 = "Hi there, how are you?"
    q2 = "How much is 6+6?"

    # Process both prompts concurrently
    results = await asyncio.gather(
        process_prompt(llama, q1, "Q1"),
        process_prompt(llama, q2, "Q2")
    )

    # Print results
    for label, prompt, answer in results:
        print(f"User: {prompt}")
        print(f"AI: {answer}\n")


if __name__ == "__main__":
    asyncio.run(main())
