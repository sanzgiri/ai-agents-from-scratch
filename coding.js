import {
    getLlama,
    LlamaChatSession,
} from "node-llama-cpp";
import {fileURLToPath} from "url";
import path from "path";
import { performance } from "node:perf_hooks";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const llama = await getLlama();
const model = await llama.loadModel({
    modelPath: path.join(
        __dirname,
        "models",
        //"DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"
        "hf_giladgd_gpt-oss-20b.MXFP4.gguf"
    )
});
const context = await model.createContext();
const session = new LlamaChatSession({
    contextSequence: context.getSequence(),
});

const q1 = `What is hoisting in JavaScript? Explain with examples.`;

console.log('context.contextSize', context.contextSize)

// metrics
let ttftMs;
let tokensOut = 0;
const tStart = performance.now();

const a1 = await session.prompt(q1, {
    // Tip: let the lib choose or cap reasonably; using the whole context size can be wasteful
    maxTokens: Math.min(512, context.contextSize),

    // Fires as soon as the first characters arrive
    onTextChunk: (text) => {
        if (ttftMs === undefined) {
            ttftMs = performance.now() - tStart;
            console.log(`\nTTFT: ${ttftMs.toFixed(0)} ms`);
        }
        process.stdout.write(text); // optional: live print
    },

    // If you prefer counting actual tokens:
    onToken: (tokens) => {
        tokensOut += tokens.length;
    },
});

const tEnd = performance.now();
const totalMs = tEnd - tStart;
const genMs = ttftMs !== undefined ? totalMs - ttftMs : totalMs;
const tps = genMs > 0 ? (tokensOut / (genMs / 1000)) : 0;

console.log("\n\nFinal answer:\n", a1);
console.log(`Total time: ${totalMs.toFixed(0)} ms`);
if (ttftMs !== undefined) console.log(`TTFT: ${ttftMs.toFixed(0)} ms`);
console.log(`Tokens generated: ${tokensOut}`);
console.log(`Throughput (approx): ${tps.toFixed(2)} tok/s`);


llama.dispose()
model.dispose()
context.dispose()
session.dispose()