# Setup Guide for AI Agents From Scratch (Python)

This guide will help you set up your environment to run the Python examples in this repository.

## Prerequisites

- **Python 3.8 or higher** (3.10+ recommended)
- **8GB RAM minimum** (16GB recommended)
- **C++ compiler** (for building llama-cpp-python)
- **Git** (to clone the repository)

## Step 1: Clone the Repository

```bash
git clone https://github.com/sanzgiri/ai-agents-from-scratch.git
cd ai-agents-from-scratch
```

## Step 2: Create a Virtual Environment (Recommended)

### Using venv (Python built-in):

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/Mac:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

### Using conda:

```bash
conda create -n ai-agents python=3.10
conda activate ai-agents
```

## Step 3: Install Dependencies

### Basic Installation (CPU Only):

```bash
pip install -r requirements.txt
```

### GPU Acceleration (Optional but Recommended):

#### For NVIDIA GPUs (CUDA):

```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
pip install openai python-dotenv
```

#### For Apple Silicon (Metal):

```bash
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
pip install openai python-dotenv
```

#### For AMD GPUs (ROCm):

```bash
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
pip install openai python-dotenv
```

### Optimized CPU Installation:

For better CPU performance with BLAS support:

```bash
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python --force-reinstall --no-cache-dir
pip install openai python-dotenv
```

## Step 4: Download Models

You need to download GGUF format models and place them in the `models/` directory.

### Create models directory:

```bash
mkdir -p models
```

### Recommended Models:

See [DOWNLOAD.md](DOWNLOAD.md) for detailed model download instructions.

#### Quick Start Models (smaller, faster):

1. **Qwen3-1.7B-Q8_0.gguf** (~1.8GB)
   - Used in: intro, simple-agent, simple-agent-with-memory, think
   - Download from: [Hugging Face](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF)

2. **hf_giladgd_gpt-oss-20b.MXFP4.gguf** (~12GB)
   - Used in: coding, react-agent
   - Better for complex reasoning tasks

#### Example download using huggingface-cli:

```bash
# Install huggingface hub
pip install huggingface-hub

# Download a model
huggingface-cli download \
  Qwen/Qwen2.5-1.5B-Instruct-GGUF \
  qwen2.5-1.5b-instruct-q8_0.gguf \
  --local-dir ./models \
  --local-dir-use-symlinks False
```

#### Or download manually:

Visit [Hugging Face GGUF Models](https://huggingface.co/models?library=gguf) and download models to the `models/` directory.

## Step 5: Set Up Environment Variables (Optional)

For OpenAI examples, create a `.env` file:

```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

## Step 6: Verify Installation

Test your setup with the simplest example:

```bash
python intro/intro.py
```

If successful, you should see an AI response!

## Step 7: Run Examples

Run examples in order:

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

## Troubleshooting

### Issue: "No module named 'llama_cpp'"

**Solution:** Make sure you've activated your virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or conda activate ai-agents
pip install -r requirements.txt
```

### Issue: llama-cpp-python installation fails

**Solution 1:** Install build tools

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install build-essential cmake
```

**On macOS:**
```bash
xcode-select --install
brew install cmake
```

**On Windows:**
- Install Visual Studio Build Tools
- Install CMake from https://cmake.org/download/

**Solution 2:** Use pre-built wheels:
```bash
pip install llama-cpp-python --prefer-binary
```

### Issue: "Model not found"

**Solution:** Make sure models are in the correct directory:
```bash
ls -la models/
# Should show your .gguf files
```

Update model paths in Python files if needed.

### Issue: Out of memory errors

**Solution:** 
1. Use smaller quantized models (Q4_K_M instead of Q8_0)
2. Reduce context size in the code:
   ```python
   llama = Llama(
       model_path="...",
       n_ctx=1024,  # Reduce from 2048
       verbose=False
   )
   ```
3. Close other applications to free up RAM

### Issue: Slow inference

**Solutions:**
1. Install with GPU support (see Step 3)
2. Use quantized models (Q4_K_M or Q5_K_M)
3. Reduce max_tokens in completions
4. Consider using smaller models

### Issue: Function calling not working

**Cause:** Some smaller models don't support function calling well.

**Solution:** 
- Use models specifically trained for function calling
- Try larger models (7B+ parameters)
- Check model documentation for function calling support

## Performance Tips

1. **Use GPU acceleration** if available (massive speedup)
2. **Start with smaller models** (1.5B-3B) for learning
3. **Quantization levels:**
   - Q4_K_M: Smallest, fastest, good quality
   - Q5_K_M: Balanced
   - Q8_0: Best quality, largest size
4. **Adjust context size** based on your needs (smaller = faster)
5. **Batch processing** for multiple requests (see batch.py)

## System Requirements by Model Size

| Model Size | RAM Required | VRAM (GPU) | Speed (CPU) |
|------------|--------------|------------|-------------|
| 1.5B Q4    | 2GB          | 1GB        | Fast        |
| 3B Q4      | 4GB          | 2GB        | Medium      |
| 7B Q4      | 8GB          | 4GB        | Slow        |
| 13B Q4     | 16GB         | 8GB        | Very Slow   |
| 20B+       | 32GB+        | 12GB+      | Extremely Slow |

## Additional Resources

- **llama-cpp-python documentation**: https://llama-cpp-python.readthedocs.io/
- **Model hub**: https://huggingface.co/models?library=gguf
- **GGUF format info**: https://github.com/ggerganov/ggml/blob/master/docs/gguf.md
- **Python conversion guide**: [PYTHON_CONVERSION.md](PYTHON_CONVERSION.md)

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Review [PYTHON_CONVERSION.md](PYTHON_CONVERSION.md) for API differences
3. Check model compatibility with your system
4. Open an issue on GitHub with:
   - Your Python version (`python --version`)
   - Your OS
   - Error messages
   - Steps to reproduce

## Next Steps

Once setup is complete:

1. Read [README.md](README.md) for learning path
2. Start with `intro/intro.py`
3. Work through examples in order
4. Read CODE.md and CONCEPT.md in each directory
5. Experiment with different models and parameters

Happy learning! 🚀
