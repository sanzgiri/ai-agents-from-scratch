# Node.js to Python Conversion Guide

This document outlines the key differences between the Node.js and Python implementations of the AI Agents examples.

## Key Library Changes

| Node.js | Python |
|---------|--------|
| `node-llama-cpp` | `llama-cpp-python` |
| `openai` (npm) | `openai` (PyPI) |
| `dotenv` | `python-dotenv` |

## Installation

**Node.js:**
```bash
npm install
```

**Python:**
```bash
pip install -r requirements.txt
```

## Running Examples

**Node.js:**
```bash
node intro/intro.js
```

**Python:**
```bash
python intro/intro.py
```

## Code Structure Differences

### 1. Model Initialization

**Node.js:**
```javascript
import { getLlama } from "node-llama-cpp";

const llama = await getLlama();
const model = await llama.loadModel({ modelPath: "..." });
const context = await model.createContext();
const session = new LlamaChatSession({
    contextSequence: context.getSequence(),
});
```

**Python:**
```python
from llama_cpp import Llama

llama = Llama(
    model_path="...",
    n_ctx=2048,
    verbose=False
)
```

### 2. Creating Chat Completions

**Node.js:**
```javascript
const response = await session.prompt(prompt);
```

**Python:**
```python
response = llama.create_chat_completion(
    messages=[
        {"role": "user", "content": prompt}
    ]
)
answer = response["choices"][0]["message"]["content"]
```

### 3. Function/Tool Calling

**Node.js:**
```javascript
const getCurrentTime = defineChatSessionFunction({
    description: "Get the current time",
    params: {
        type: "object",
        properties: {}
    },
    async handler() {
        return new Date().toLocaleTimeString();
    }
});

const functions = { getCurrentTime };
const response = await session.prompt(prompt, { functions });
```

**Python:**
```python
def get_current_time() -> str:
    """Get the current time"""
    return datetime.now().strftime("%I:%M:%S %p")

functions = [{
    "name": "get_current_time",
    "description": "Get the current time",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}]

response = llama.create_chat_completion(
    messages=messages,
    tools=functions,
    tool_choice="auto"
)

# Handle tool calls
if "tool_calls" in response["choices"][0]["message"]:
    # Execute function and continue conversation
    ...
```

### 4. Streaming Responses

**Node.js:**
```javascript
const response = await session.prompt(prompt, {
    maxTokens: 2000,
    onTextChunk: (text) => {
        process.stdout.write(text);
    },
});
```

**Python:**
```python
response = llama.create_chat_completion(
    messages=[{"role": "user", "content": prompt}],
    max_tokens=2000,
    stream=True
)

for chunk in response:
    if "choices" in chunk:
        delta = chunk["choices"][0].get("delta", {})
        if "content" in delta:
            print(delta["content"], end="", flush=True)
```

### 5. Memory Management

**Node.js:**
```javascript
import fs from 'fs/promises';

export class MemoryManager {
    async loadMemories() {
        const data = await fs.readFile(this.memoryFilePath, 'utf-8');
        return JSON.parse(data);
    }
}
```

**Python:**
```python
import json
from pathlib import Path

class MemoryManager:
    def load_memories(self):
        with open(self.memory_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
```

### 6. Async/Parallel Processing

**Node.js:**
```javascript
const [a1, a2] = await Promise.all([
    session1.prompt(q1),
    session2.prompt(q2)
]);
```

**Python:**
```python
import asyncio

async def process_prompt(llama, prompt):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: llama.create_chat_completion(...)
    )

results = await asyncio.gather(
    process_prompt(llama, q1),
    process_prompt(llama, q2)
)
```

### 7. File Paths

**Node.js:**
```javascript
import { fileURLToPath } from "url";
import path from "path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const modelPath = path.join(__dirname, "..", "models", "model.gguf");
```

**Python:**
```python
from pathlib import Path

current_dir = Path(__file__).parent
model_path = current_dir / ".." / "models" / "model.gguf"
# or
model_path = str(current_dir / ".." / "models" / "model.gguf")
```

## Important Notes

### Context Management

**Node.js** (`node-llama-cpp`):
- Explicit context and session management
- Supports multiple sequences for parallel processing
- Built-in chat session wrapper

**Python** (`llama-cpp-python`):
- Simpler API with integrated context management
- Uses message-based API (OpenAI-compatible)
- Function calling handled through `tools` parameter

### Function Calling

The Python implementation uses the OpenAI-compatible function calling format:
1. Define functions as dictionaries with JSON schema
2. Pass them via the `tools` parameter
3. Check response for `tool_calls`
4. Execute functions manually
5. Add function results back to message history
6. Continue conversation

### Cleanup

**Node.js** requires explicit disposal:
```javascript
llama.dispose();
model.dispose();
context.dispose();
session.dispose();
```

**Python** handles cleanup automatically (though you can manually delete objects if needed).

## File Naming Conventions

All `.js` files have been converted to `.py` files:
- `intro.js` → `intro.py`
- `simple-agent.js` → `simple-agent.py`
- `memory-manager.js` → `memory_manager.py` (Python convention: snake_case)
- `prompt-debugger.js` → `prompt_debugger.py`

## Testing Your Conversion

Run each example in order to verify the conversion:

```bash
# Basic examples
python intro/intro.py
python translation/translation.py
python think/think.py
python coding/coding.py
python batch/batch.py

# Agent examples (require function calling support)
python simple-agent/simple-agent.py
python simple-agent-with-memory/simple-agent-with-memory.py
python react-agent/react-agent.py

# OpenAI examples (require API key)
python openai-intro/openai-intro.py
```

## Common Issues

1. **Model path errors**: Ensure models are in the `models/` directory
2. **Import errors**: Make sure `llama-cpp-python` is installed correctly
3. **Function calling**: Some smaller models may not support function calling well
4. **Memory**: Ensure you have enough RAM for the models you're using

## Further Reading

- [llama-cpp-python Documentation](https://llama-cpp-python.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
