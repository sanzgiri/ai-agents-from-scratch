# Running AI Agents in GitHub Codespaces

This guide explains how to run and test the Python examples in GitHub Codespaces.

## Quick Start in Codespaces

1. **Open in Codespaces:**
   - Click the green "Code" button on GitHub
   - Select "Codespaces" tab
   - Click "Create codespace on main"

2. **Wait for Setup:**
   - The dev container will automatically install Python dependencies
   - This takes 2-3 minutes on first launch

3. **Download a Small Model (Required):**
   ```bash
   # Create models directory
   mkdir -p models
   
   # Download a small test model (using huggingface-cli)
   pip install huggingface-hub
   huggingface-cli download \
     Qwen/Qwen2.5-1.5B-Instruct-GGUF \
     qwen2.5-1.5b-instruct-q8_0.gguf \
     --local-dir ./models \
     --local-dir-use-symlinks False
   
   # Rename to match expected name
   mv models/qwen2.5-1.5b-instruct-q8_0.gguf models/Qwen3-1.7B-Q8_0.gguf
   ```

4. **Run Your First Example:**
   ```bash
   python intro/intro.py
   ```

## What's Pre-configured

The `.devcontainer/devcontainer.json` automatically sets up:

- ✅ Python 3.11
- ✅ All required Python packages (`llama-cpp-python`, `openai`, `python-dotenv`)
- ✅ VS Code Python extensions
- ✅ Git and GitHub CLI

## Running Examples in Codespaces

### Basic Examples (No Model Download Required for Syntax Testing)

Test that Python files are valid:
```bash
# Check syntax
python -m py_compile intro/intro.py
python -m py_compile simple-agent/simple-agent.py
```

### With Models (Full Execution)

Once you've downloaded models:

```bash
# Basic LLM interaction
python intro/intro.py

# Specialized behavior
python translation/translation.py

# Reasoning
python think/think.py

# Streaming
python coding/coding.py

# Agents with function calling
python simple-agent/simple-agent.py
python simple-agent-with-memory/simple-agent-with-memory.py
python react-agent/react-agent.py
```

### OpenAI Examples (Requires API Key)

1. Create a `.env` file:
   ```bash
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```

2. Run OpenAI examples:
   ```bash
   python openai-intro/openai-intro.py
   ```

## Codespaces Limitations & Tips

### Resource Constraints

**Free Tier:**
- 2 cores, 4GB RAM
- 15-32GB storage
- 120 hours/month for personal accounts

**Implications:**
- ✅ Can run small models (1.5B-3B parameters)
- ⚠️ Larger models (7B+) may be slow or fail due to memory
- ⚠️ No GPU acceleration (CPU only)

### Recommended Models for Codespaces

| Model | Size | RAM Usage | Codespaces Compatible |
|-------|------|-----------|----------------------|
| Qwen2.5-1.5B Q4 | ~900MB | ~2GB | ✅ Yes (fast) |
| Qwen2.5-1.5B Q8 | ~1.6GB | ~3GB | ✅ Yes (slower) |
| Phi-3-mini Q4 | ~2GB | ~3GB | ⚠️ Marginal |
| Llama-3-8B Q4 | ~4.3GB | ~6GB | ❌ Too large |

### Performance Tips

1. **Use Q4 quantization** instead of Q8 for faster inference
2. **Reduce context size** in code:
   ```python
   llama = Llama(
       model_path="...",
       n_ctx=512,  # Smaller than default 2048
       n_threads=2,  # Match Codespaces cores
       verbose=False
   )
   ```
3. **Reduce max_tokens** in completions:
   ```python
   response = llama.create_chat_completion(
       messages=[...],
       max_tokens=100  # Shorter responses
   )
   ```

## Testing Without Models

You can verify Python code without downloading models:

```bash
# Run syntax checks
python -m py_compile intro/intro.py

# Test imports
python -c "from llama_cpp import Llama; print('Success!')"

# Run type checking (if mypy installed)
pip install mypy
mypy intro/intro.py --ignore-missing-imports
```

## Downloading Models in Codespaces

### Option 1: Hugging Face CLI (Recommended)

```bash
# Install CLI
pip install huggingface-hub

# Download specific file
huggingface-cli download \
  Qwen/Qwen2.5-1.5B-Instruct-GGUF \
  qwen2.5-1.5b-instruct-q4_k_m.gguf \
  --local-dir ./models \
  --local-dir-use-symlinks False
```

### Option 2: Direct Download with wget

```bash
# Example: Download from Hugging Face
wget -P models/ \
  https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf
```

### Option 3: Use Smaller Models

Look for models specifically optimized for limited resources:
- Qwen2.5-1.5B
- Phi-3-mini
- TinyLlama-1.1B

## Persistent Storage

⚠️ **Important:** Codespaces storage is ephemeral by default!

### Keep Models Across Sessions:

1. **Commit models to a separate branch** (not recommended for large files)
2. **Use GitHub LFS** for model storage
3. **Download on each session** (preferred for Codespaces)

### Save Your Work:

```bash
# Commit code changes
git add .
git commit -m "Your changes"
git push
```

## Troubleshooting in Codespaces

### "Out of Memory" Error

**Solutions:**
1. Use smaller models (1.5B Q4)
2. Reduce `n_ctx` to 256-512
3. Close unused browser tabs
4. Restart Codespace

### Models Download Too Slow

**Solutions:**
1. Use smaller quantized versions (Q4 instead of Q8)
2. Download overnight
3. Consider upgrading Codespace tier for better bandwidth

### "llama-cpp-python" Installation Fails

**Solutions:**
```bash
# Rebuild with pre-built wheels
pip install llama-cpp-python --prefer-binary --force-reinstall
```

Or use the lightweight version:
```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

### Codespace Runs Slow

- Free tier Codespaces use 2 cores
- Inference will be slower than local GPU
- Expect 2-5 tokens/second for 1.5B models

## CI/CD Testing

The repository includes GitHub Actions that test:
- ✅ Python syntax validation
- ✅ Import checks
- ✅ Multiple Python versions (3.9, 3.10, 3.11)

See `.github/workflows/test-python.yml` for details.

## Alternative: Local Development

For better performance with larger models:
1. Clone repo locally
2. Follow [SETUP.md](SETUP.md) for local setup
3. Use GPU acceleration if available

Codespaces is great for:
- ✅ Learning and experimentation
- ✅ Small model testing
- ✅ Code development and debugging
- ✅ Quick demos

Local setup is better for:
- 🚀 Production workloads
- 🚀 Large models (7B+)
- 🚀 GPU acceleration
- 🚀 Frequent usage

## Resources

- **Codespaces Docs**: https://docs.github.com/en/codespaces
- **Dev Containers**: https://containers.dev/
- **llama-cpp-python**: https://github.com/abetlen/llama-cpp-python
- **Model Hub**: https://huggingface.co/models?library=gguf

## Getting Help

If you encounter Codespaces-specific issues:
1. Check this guide
2. Review Codespace logs (View → Output → Codespaces)
3. Try rebuilding container (Command Palette → "Rebuild Container")
4. Open an issue with "Codespaces" label

Happy coding in the cloud! ☁️
