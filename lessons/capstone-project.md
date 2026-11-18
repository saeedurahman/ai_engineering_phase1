# 🏆 Final Capstone Project: Multi-Provider AI Business Assistant

**Course:** AI Engineering Foundations – From Fundamentals to Production-Ready AI Applications  
**Student:** Professional Software Developer (Flutter, Python, Next.js)  
**Status:** 🚀 IN PROGRESS (Step 1: Architecture & Config)  

---

## 🎯 Capstone Project Vision
Ek modular, production-grade **Autonomous AI Business Assistant** build karna jo:
1. **Multi-Provider & Model Switching:** Groq Cloud (`qwen/qwen3.8-27b`) aur Local Ollama (`llama3.2:1b`, `qwen2.5:0.5b`) dono par chale.
2. **Autonomous Tool / Function Calling:** Courier order database se real-time shipping tracking lookup kare.
3. **Structured Outputs:** Clean JSON schema delivery.
4. **Context Sliding Window Memory:** Zero context overflow aur flat token cost.
5. **Live Telemetry & Cost Metering:** Har message par tokens, latency, aur exact dollar ($) cost calculate kare.
6. **Automatic Cloud-to-Local Failover:** Cloud down hone par bina crash hue local hardware par auto-switch ho.
7. **Bilingual:** Professional Pakistani Roman Urdu aur English support.
8. **Automated Pytest Suite:** Pre-deployment quality evals.
9. **GitHub-Ready Portfolio:** Professional `README.md` with architecture diagrams.

---

## 🏗️ Clean Modular Project Architecture

```text
phase1-2/
│
└── capstone/
    ├── __init__.py
    ├── config.py           # Centralized configuration, models, pricing, and system prompts
    ├── tools.py            # Mock Database, Python functions & OpenAI-compatible Tool Schemas
    ├── client.py           # Provider-Agnostic Client (Groq + Ollama + Auto-Failover)
    ├── logger.py           # Structured JSONL Audit Logger & Telemetry Cost Meter
    ├── agent.py            # Core Agent: Function Calling loop + Sliding Window + Streaming
    ├── app.py              # Interactive Terminal UI Application
    └── test_capstone.py    # Automated Pytest Regression & Evals Suite
```
