import {
    getLlama, resolveModelFile, LlamaChatSession,
    HarmonyChatWrapper
} from "node-llama-cpp";
import {fileURLToPath} from "url";
import path from "path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// const modelUri = "hf:giladgd/gpt-oss-20b-GGUF/gpt-oss-20b.MXFP4.gguf";
// hf:mradermacher/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M

const llama = await getLlama();
const model = await llama.loadModel({
    modelPath: path.join(
        __dirname,
        "models",
        "hf_giladgd_gpt-oss-20b.MXFP4.gguf"
    )
});

/*
const model = await llama.loadModel({
    modelPath: await resolveModelFile(
        modelUri,
        path.join(__dirname, "models")
    )
});
 */

const context = await model.createContext();
const session = new LlamaChatSession({
    contextSequence: context.getSequence(),
    chatWrapper: new HarmonyChatWrapper({
        modelIdentity: "You are ChatGPT, a large language model trained by OpenAI.",
        reasoningEffort: "high"
    })
});

const q1 = "My name is Jungjun";
console.log("User: " + q1);

const a1 = await session.prompt(q1);
console.log("AI: " + a1);

const q2 = "What is my name?";
console.log("User: " + q2);

const a2 = await session.prompt(q2);
console.log("AI: " + a2);

// console.log(session.getChatHistory())
// session.setChatHistory(chatHistory: ChatHistoryItem[])
// session.resetChatHistory()

llama.dispose()
model.dispose()
context.dispose()
session.dispose()