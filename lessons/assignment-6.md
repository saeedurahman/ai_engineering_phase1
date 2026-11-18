# Week 1 — Module 6 — Practical Assignment 6

**Course:** AI Engineering Foundations  
**Module:** 6 — Ollama: Local AI Models (Offline AI, Privacy & On-Device Inference)  
**Status:** ⏳ Pending Student Implementation  

---

## 🎯 Objective
1. Windows machine par **Ollama** locally install aur verify karna.
2. Ek lightweight quantized model (`llama3.2:1b` ya `qwen2.5:1.5b`) pull karke locally chalana.
3. Python script ke zariye **Localhost (Port 11434)** par chalne wale AI model se offline baat karna (OpenAI-compatible pattern).
4. Response time aur generation speed (tokens/sec) measure karna.

---

## 🛠️ Step-by-Step Milestones
- **Milestone 1:** Install Ollama Windows (`https://ollama.com/download`).
- **Milestone 2:** Verify via terminal: `ollama --version`.
- **Milestone 3:** Pull lightweight model: `ollama pull llama3.2:1b` (Size: ~1.3 GB).
- **Milestone 4:** Terminal chat test: `ollama run llama3.2:1b`.
- **Milestone 5:** Python integration script `assignment_6.py` with latency & offline test.

---

## ⚙️ Acceptance Criteria
- Ollama service running locally on `http://localhost:11434`.
- Python script successfully connects to local Ollama without internet API keys.
- Streaming response received directly from local hardware.
