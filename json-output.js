import {
    getLlama,
    LlamaChatSession,
    DeepSeekChatWrapper
} from "node-llama-cpp";
import {fileURLToPath} from "url";
import path from "path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const llama = await getLlama();
const model = await llama.loadModel({
    modelPath: path.join(
        __dirname,
        "models",
        "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"
    )
});
const context = await model.createContext();
const session = new LlamaChatSession({
    contextSequence: context.getSequence(),
    //chatWrapper: new DeepSeekChatWrapper()
});
const grammar = await llama.getGrammarFor("json");

const q1 = `You are a JSON generator.
Output ONLY valid JSON — no explanations, no markdown, no text outside the JSON.

Generate a JSON ARRAY containing two objects.
The JSON output must start with [ and end with ].

The array must contain EXACTLY 2 objects.

Each object must include the following fields with realistic random values:
- username
- email
- confirmed
- firstname
- lastname
- age
- height
- weight`;

console.log('context.contextSize', context.contextSize)
const a1 = await session.prompt(q1, {
    grammar,
    maxTokens: context.contextSize
});

console.log(JSON.parse(a1));


llama.dispose()
model.dispose()
context.dispose()
session.dispose()