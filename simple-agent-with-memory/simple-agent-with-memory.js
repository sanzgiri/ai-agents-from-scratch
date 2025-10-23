import {defineChatSessionFunction, getLlama, LlamaChatSession} from "node-llama-cpp";
import {fileURLToPath} from "url";
import path from "path";
import {MemoryManager} from "./memory-manager.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const llama = await getLlama({debug: false});
const model = await llama.loadModel({
    modelPath: path.join(__dirname, "../", "models", "Qwen3-1.7B-Q8_0.gguf")
});
const context = await model.createContext({contextSize: 2000});

// Initialize memory manager
const memoryManager = new MemoryManager('./agent-memory.json');

// Load existing memories and add to system prompt
const memorySummary = await memoryManager.getMemorySummary();

const systemPrompt = `You are a helpful assistant with long-term memory.
${memorySummary}

When the user shares important information about themselves, their preferences, or facts 
they want you to remember, use the saveMemory function to store it.`;

const session = new LlamaChatSession({
    contextSequence: context.getSequence(),
    systemPrompt,
});

// Function to save memories
const saveMemory = defineChatSessionFunction({
    description: "Save important information to long-term memory (user preferences, facts, personal details)",
    params: {
        type: "object",
        properties: {
            type: {
                type: "string",
                enum: ["fact", "preference"],
                description: "Type of memory to save"
            },
            content: {
                type: "string",
                description: "The information to remember"
            },
            key: {
                type: "string",
                description: "For preferences: the preference key (e.g., 'favorite_color')"
            }
        },
        required: ["type", "content"]
    },
    async handler(params) {
        if (params.type === "fact") {
            await memoryManager.addFact(params.content);
            return "Fact saved to memory";
        } else if (params.type === "preference") {
            const key = params.key || params.content.split(' ')[0];
            await memoryManager.addPreference(key, params.content);
            return "Preference saved to memory";
        }
    }
});

const functions = {saveMemory};

// Example conversation
const prompt1 = "Hi! My name is Alex and I love pizza.";
const response1 = await session.prompt(prompt1, {functions});
console.log("AI: " + response1);

// Later conversation (even after restarting the script)
const prompt2 = "What's my favorite food?";
const response2 = await session.prompt(prompt2, {functions});
console.log("AI: " + response2);

// Clean up
llama.dispose();
model.dispose();
context.dispose();
session.dispose();