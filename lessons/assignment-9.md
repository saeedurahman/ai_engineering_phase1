# Week 2 — Module 9 — Practical Assignment 9

**Course:** AI Engineering Foundations  
**Module:** 9 — Build a Professional AI Chatbot (Urdu/English Business Assistant)  
**Status:** ⏳ Pending Student Implementation  

---

## 🎯 Objective
Ek mukammal, production-grade **Bilingual (Roman Urdu/English) Business Chatbot** build karna jo:
1. **Provider Flexibility:** User ko startup par Groq Cloud ya Local Ollama choose karne ka ikhtiyar de.
2. **Context Sliding Window:** Hamesha System Prompt ko protect kare aur sirf aakhri 6 messages bhej kar token bill ko flat aur predictable rakhe.
3. **Real-Time Streaming:** Typewriter effect ke sath responsive UX provide kare.
4. **Live Telemetry & Cost Metering:** Har message ke baad tokens aur exact dollar cost calculate karke print kare.
5. **Persistent Audit Logging:** Har turn ko structured `chat_audit_log.jsonl` file mein timestamp ke sath persist kare.
6. **Session Summary:** Session end hone par cumulative analytics report display kare.

---

## 🛠️ Components
- **Engine:** `UnifiedAIClient` (Groq / Ollama)
- **Memory Engine:** Sliding Window Pruner
- **Telemetry Engine:** Token & Cost Tracker
- **Audit Logger:** JSONL File Writer

---

## ⚙️ Acceptance Criteria
- Clean, modular Python script (`assignment_9.py`).
- Flawless streaming in Roman Urdu/English.
- Verified entries created in `chat_audit_log.jsonl`.
- Zero context window overflow during extended chat.
