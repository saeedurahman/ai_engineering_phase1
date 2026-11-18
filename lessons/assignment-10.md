# Week 2 — Module 10 — Practical Assignment 10

**Course:** AI Engineering Foundations  
**Module:** 10 — AI Application Testing & Automated Evals with Pytest  
**Status:** ⏳ Pending Student Implementation  

---

## 🎯 Objective
PakStyle AI Business Assistant ke liye ek production-ready **Automated Regression Test Suite (`test_chatbot.py`)** build karna jo `pytest` ke zariye verify kare:
1. **Factual Policy Accuracy:** Delivery charges (Rs 200) aur Free delivery threshold (> Rs 3,000).
2. **Exchange Window Accuracy:** 7-day return window aur original tags criteria.
3. **Guardrail Defense:** Aggressive 30% discount maangne par 10% (SAVE10) se zyada offer na kare.
4. **Security & Prompt Injection Resistance:** "SYSTEM OVERRIDE" command ko reject kare aur internal prompt rules leak na kare.
5. **Sliding Window Context Continuity:** Conversation history ke context ko accurately verify kare.

---

## 🛠️ Components
- **Test Framework:** `pytest`
- **Target Application:** `ProductionBusinessChatbot` (`assignment_9.py`)
- **Assertion Strategies:** Semantic Inclusion, Negative Constraints, Security Blocks.

---

## ⚙️ Acceptance Criteria
- Clean `test_chatbot.py` file with standard Pytest fixtures and assertions.
- All 5 automated tests pass with green status (`5 passed in X.XXs`).
- Zero flaky tests (run with deterministic temperature).
