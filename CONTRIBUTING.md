# Contributing Guidelines

Thank you for considering contributing to AI Agents from Scratch!

## 🎯 Project Philosophy

This repository teaches AI agent fundamentals by building from scratch. Every contribution should support this learning mission.

**Core Principles:**
- **Clarity over cleverness** - Code should be easy to understand
- **Fundamentals first** - No black boxes or magic
- **Progressive learning** - Each example builds on the previous
- **Local-first** - No API dependencies

## 🤝 Types of Contributions

### 🐛 Bug Reports
Found something broken? Open an issue with:
- Which example (`intro/`, `react-agent/`, etc.)
- What you expected vs. what happened
- Your environment (Node version, OS, model used)
- Steps to reproduce

### 📝 Documentation Improvements
- Typos and grammar fixes
- Clearer explanations
- Better code comments
- Additional examples in documentation
- Diagrams and visualizations

### 💡 New Examples
Want to add a new agent pattern? Great! Please:
1. **Open an issue first** - let's discuss if it fits
2. Follow the existing structure:
    - `pattern-name/pattern-name.js` - Working code
    - `pattern-name/CODE.md` - Detailed code walkthrough
    - `pattern-name/CONCEPT.md` - Why it matters, use cases
3. Keep it simple and well-commented
4. Test thoroughly with at least one model

### 🔧 Code Improvements
- Performance optimizations (with benchmarks)
- Better error handling
- Clearer variable names
- More helpful console output

## 🚫 What We're Not Looking For

- Framework integrations (LangChain, etc.) - this repo teaches what they do
- Cloud API examples - keep it local
- Production features (monitoring, scaling) - this is educational
- Complex abstractions - keep it beginner-friendly

## 📋 Contribution Process

1. **Fork** the repository
2. **Create a branch**: `git checkout -b fix/issue-description`
3. **Make changes** and test thoroughly
4. **Commit** with clear messages: `git commit -m "Fix: clarify ReAct loop explanation"`
5. **Push**: `git push origin fix/issue-description`
6. **Open a Pull Request** with:
    - Clear title
    - Description of what changed and why
    - Which issue it addresses (if any)

## ✅ Code Standards

- Use clear, descriptive variable names
- Add comments explaining *why*, not just *what*
- Follow existing code style (no linter, just match the patterns)
- Keep examples self-contained (one file when possible)
- Test with Qwen or Llama models before submitting

## 📚 Documentation Standards

- Use clear, simple language
- Explain concepts before code
- Include diagrams where helpful (ASCII art is fine!)
- Provide real-world use cases
- Link to related examples

## 🎨 Example Structure
```
new-pattern/
├── new-pattern.js          # The working code
├── CODE.md                 # Line-by-line walkthrough
└── CONCEPT.md              # High-level explanation
```

**CODE.md should include:**
- Prerequisites
- Step-by-step code breakdown
- How to run it
- Expected output

**CONCEPT.md should include:**
- What problem it solves
- Why this pattern matters
- Real-world applications
- Simple diagrams

## 💬 Getting Help

- Not sure if your idea fits? **Open an issue to discuss**
- Stuck on implementation? **Ask in the issue**
- Want to pair on something? **Reach out!**

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

## 🙏 Recognition

All contributors will be recognized in the README. Thank you for helping others learn!

---

**Questions?** Open an issue or reach out. Happy to help guide your contribution! 🚀