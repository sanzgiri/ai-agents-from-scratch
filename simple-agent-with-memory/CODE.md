# Code Explanation: simple-agent-with-memory.js

This example extends the simple agent with **persistent memory**, enabling it to remember information across sessions.

## Key Components

### 1. MemoryManager Import
```javascript
import {MemoryManager} from "./memory-manager.js";
```
Custom class for persisting agent memories to JSON files.

### 2. Initialize Memory Manager
```javascript
const memoryManager = new MemoryManager('./agent-memory.json');
const memorySummary = await memoryManager.getMemorySummary();
```
- Loads existing memories from file
- Generates summary for system prompt

### 3. Memory-Aware System Prompt
```javascript
const systemPrompt = `You are a helpful assistant with long-term memory.
${memorySummary}

When the user shares important information about themselves, their preferences, or facts 
they want you to remember, use the saveMemory function to store it.`;
```
- Includes existing memories in prompt
- Instructs agent when to save new memories

### 4. saveMemory Function
```javascript
const saveMemory = defineChatSessionFunction({
    description: "Save important information to long-term memory",
    params: {
        type: "object",
        properties: {
            type: { type: "string", enum: ["fact", "preference"] },
            content: { type: "string" },
            key: { type: "string" }
        },
        required: ["type", "content"]
    },
    async handler(params) {
        if (params.type === "fact") {
            await memoryManager.addFact(params.content);
        } else if (params.type === "preference") {
            await memoryManager.addPreference(params.key, params.content);
        }
        return "Memory saved";
    }
});
```

**What it does:**
- Saves facts (general information)
- Saves preferences (key-value pairs)
- Persists to JSON file

### 5. Example Conversation
```javascript
const prompt1 = "Hi! My name is Alex and I love pizza.";
const response1 = await session.prompt(prompt1, {functions});
// Agent calls saveMemory to store this information

const prompt2 = "What's my favorite food?";
const response2 = await session.prompt(prompt2, {functions});
// Agent recalls from memory: "Pizza"
```

## How Memory Works

### Flow Diagram
```
Session 1:
User: "My name is Alex"
  ↓
Agent calls: saveMemory(type="fact", content="User's name is Alex")
  ↓
Saved to: agent-memory.json

Session 2 (after restart):
1. Load memories from agent-memory.json
2. Add to system prompt
3. Agent knows: "User's name is Alex"
4. Can use this information
```

## The MemoryManager Class

Located in `memory-manager.js`:

```javascript
class MemoryManager {
  async loadMemories()       // Load from JSON
  async saveMemories()       // Write to JSON
  async addFact()           // Add general fact
  async addPreference()     // Add key-value preference
  async getMemorySummary()  // Format for system prompt
}
```

## Key Concepts

### 1. Persistent State
- Memories survive script restarts
- Stored in JSON file
- Loaded at startup

### 2. Memory Types
- **Facts**: General information ("User lives in Paris")
- **Preferences**: Key-value pairs ("favorite_color": "blue")

### 3. Memory Integration
Memories are injected into system prompt:
```
System: You are a helpful assistant.

=== LONG-TERM MEMORY ===
Known Facts:
- User's name is Alex
- User loves pizza

User Preferences:
- favorite_color: blue
```

## Why This Matters

Without memory: Each conversation starts from scratch
With memory: Agent remembers context, preferences, past interactions

This enables:
- Personalized responses
- Contextual conversations
- Long-term relationships
- Stateful agents

## Expected Output

First run:
```
User: "Hi! My name is Alex and I love pizza."
AI: "Nice to meet you, Alex! I've noted that you love pizza."
```

Second run (after restart):
```
User: "What's my favorite food?"
AI: "Pizza! You mentioned you love it."
```

The agent remembers across sessions!
