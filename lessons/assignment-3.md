# Week 1 — Module 3 — Practical Assignment 3

**Course:** AI Engineering Foundations  
**Module:** 3 — Prompt Engineering (System Prompts, Few-Shot, Guardrails & Delimiters)  
**Status:** ⏳ Pending Student Implementation  

---

## 🎯 Objective
Ek production-grade Pakistani E-Commerce Brand (**"PakStyle Apparel"**) ke liye AI Customer Support Assistant ka structured prompt architect karna jo:
1. English aur Roman Urdu queries ko fluently handle kare.
2. Store policies (Context Injection) par strictly mabni jawab de.
3. Strict Guardrails (Discounts limit, Competitor defense, Abusive tone handling) enforce kare.
4. Prompt Injection attacks ko neutralise kare.

---

## 📋 Requirements
- File: `assignment_3.py`
- Provider: Groq API (`qwen/qwen3.8-27b`)
- Prompt Architecture:
  - `role: "system"`: Persona, Store Policies, Guardrails, aur Delimiter rules.
  - Few-Shot Examples for Roman Urdu tone grounding.
  - User Queries wrapped inside `<customer_query>...</customer_query>` delimiters.
- Temperature: `0.3` (Consistent yet conversational).

---

## 🧪 Test Scenarios
1. **Policy Inquiry:** Delivery charges and return policy in Roman Urdu.
2. **Aggressive Discount & Competitor Pressure:** Customer asking for 30% discount and threatening to buy from competitor. (Guardrail test: Max 10% discount).
3. **Prompt Injection Attack:** Malicious attempt to override system rules. (Security test).
4. **Exchange Request:** Roman Urdu product exchange inquiry.

---

## ⚙️ Acceptance Criteria
- Zero leaks of internal prompt instructions during attacks.
- Exact adherence to business rules (No discounts > 10%).
- Courteous Roman Urdu tone without breaking character.
