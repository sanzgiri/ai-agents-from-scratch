from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
# Create an API key at https://platform.openai.com/api-keys
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("=== OpenAI Intro: Understanding the Basics ===\n")

# ============================================
# EXAMPLE 1: Basic Chat Completion
# ============================================
def basic_completion():
    print("--- Example 1: Basic Chat Completion ---")

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'user', 'content': 'What is llama-cpp-python?'}
        ],
    )

    print(f"AI: {response.choices[0].message.content}")
    print("\n")


# ============================================
# EXAMPLE 2: Using System Prompts
# ============================================
def system_prompt_example():
    print("--- Example 2: System Prompts (Behavioral Control) ---")

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': 'You are a coding assistant that talks like a pirate.'},
            {'role': 'user', 'content': 'Explain what async/await does in Python.'}
        ],
    )

    print(f"AI: {response.choices[0].message.content}")
    print("\n")


# ============================================
# EXAMPLE 3: Temperature and Creativity
# ============================================
def temperature_example():
    print("--- Example 3: Temperature Control ---")

    prompt = "Write a one-sentence tagline for a coffee shop."

    # Low temperature = more focused and deterministic
    focused_response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.2,
    )

    # High temperature = more creative and varied
    creative_response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=1.5,
    )

    print(f"Low temp (0.2): {focused_response.choices[0].message.content}")
    print(f"High temp (1.5): {creative_response.choices[0].message.content}")
    print("\n")


# ============================================
# EXAMPLE 4: Conversation with Context
# ============================================
def conversation_context():
    print("--- Example 4: Multi-turn Conversation ---")

    # Build conversation history
    messages = [
        {'role': 'system', 'content': 'You are a helpful coding tutor.'},
        {'role': 'user', 'content': 'What is a coroutine in Python?'},
    ]

    # First response
    response1 = client.chat.completions.create(
        model='gpt-4o',
        messages=messages,
        max_tokens=150,
    )

    print("User: What is a coroutine in Python?")
    print(f"AI: {response1.choices[0].message.content}")

    # Add AI response to history
    messages.append(response1.choices[0].message)

    # Add follow-up question
    messages.append({'role': 'user', 'content': 'Can you show me a simple example?'})

    # Second response (with context)
    response2 = client.chat.completions.create(
        model='gpt-4o',
        messages=messages,
    )

    print("\nUser: Can you show me a simple example?")
    print(f"AI: {response2.choices[0].message.content}")
    print("\n")


# ============================================
# EXAMPLE 5: Streaming Responses
# ============================================
def streaming_example():
    print("--- Example 5: Streaming Response ---")
    print("AI: ", end="")

    stream = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'user', 'content': 'Write a haiku about programming.'}
        ],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print("\n\n")


# ============================================
# EXAMPLE 6: Token Usage and Limits
# ============================================
def token_usage_example():
    print("--- Example 6: Understanding Token Usage ---")

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'user', 'content': 'Explain recursion in 3 sentences.'}
        ],
        max_tokens=100,
    )

    print(f"AI: {response.choices[0].message.content}")
    print("\nToken usage:")
    print(f"- Prompt tokens: {response.usage.prompt_tokens}")
    print(f"- Completion tokens: {response.usage.completion_tokens}")
    print(f"- Total tokens: {response.usage.total_tokens}")
    print("\n")


# ============================================
# EXAMPLE 7: Model Comparison
# ============================================
def model_comparison():
    print("--- Example 7: Different Models ---")

    prompt = "What's 25 * 47?"

    # GPT-4o - Most capable
    gpt4_response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{'role': 'user', 'content': prompt}],
    )

    # GPT-3.5-turbo - Faster and cheaper
    gpt35_response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
    )

    print(f"GPT-4o: {gpt4_response.choices[0].message.content}")
    print(f"GPT-3.5-turbo: {gpt35_response.choices[0].message.content}")
    print("\n")


# ============================================
# Run all examples
# ============================================
def main():
    try:
        basic_completion()
        system_prompt_example()
        temperature_example()
        conversation_context()
        streaming_example()
        token_usage_example()
        model_comparison()

        print("=== All examples completed! ===")
    except Exception as error:
        print(f"Error: {str(error)}")
        if 'API key' in str(error):
            print("\nMake sure to set your OPENAI_API_KEY in a .env file")


if __name__ == "__main__":
    main()
