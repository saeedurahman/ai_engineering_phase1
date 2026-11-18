# Week 1 — Module 5 — Practical Assignment 5

**Course:** AI Engineering Foundations  
**Module:** 5 — Groq API Deep Dive (Streaming, Async, Error Resilience & Benchmarking)  
**Status:** ⏳ Pending Student Implementation  

---

## 🎯 Objective
Ek production-grade, interactive **Streaming Terminal Chatbot** build karna jo:
1. Real-time **token-by-token streaming** dikhaye (`stream=True` with typewriter effect).
2. **Multi-turn conversation history** maintain kare taake AI purani baatein yaad rakh sake.
3. **Resilient Error Handling (Exponential Backoff)** implement kare taake `RateLimitError (429)` par crash hone ke bajaye smartly retry kare.
4. Groq ke **do mukhtalif models** ke darmian speed aur latency benchmark kare.

---

## 🛠️ Components
- **Streaming Generator:** `chunk.choices[0].delta.content` extraction.
- **Resilience Wrapper:** Try/except for `RateLimitError` and `APIConnectionError` with doubling delays (`1s, 2s, 4s`).
- **Interactive Terminal Loop:** User input, conversation memory append, exit command.
- **Model Comparison:** Benchmark between `qwen/qwen3.8-27b` and `openai/gpt-oss-20b`.

---

## ⚙️ Acceptance Criteria
- Real-time visible streaming without terminal buffering.
- Conversation memory works across multiple questions.
- Clean exit without Python tracebacks.
