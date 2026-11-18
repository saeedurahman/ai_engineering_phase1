# Week 2 — Module 8 — Practical Assignment 8

**Course:** AI Engineering Foundations  
**Module:** 8 — Build a Provider-Agnostic AI Client with Automatic Failover  
**Status:** ⏳ Pending Student Implementation  

---

## 🎯 Objective
Ek reusable, production-ready **Unified AI Client** banana jo:
1. Groq Cloud aur Local Ollama dono ko aik hi standard interface (`client.generate(...)`) ke zariye chalaye.
2. Provider switch karne ke liye business logic ka aik lafz bhi tabdeel na karna pare.
3. **Automatic Failover:** Agar Cloud provider (Groq) down ho ya fail ho, toh application bina crash hue foran Local Ollama par shift ho kar user ka jawab mukammal kare.
4. Streaming support provide kare.

---

## 🛠️ Architecture
- **Class:** `UnifiedAIClient`
- **Supported Providers:** `"groq"`, `"ollama"`
- **Common Method:** `generate(messages, stream=True)`
- **Failover Logic:** Primary Fail -> Try Backup -> Return result seamlessly.

---

## ⚙️ Acceptance Criteria
- Clean OOP structure with type hints.
- Smooth switching between Groq and Ollama via parameter/env.
- Successful automatic failover when Cloud is simulated as down.
