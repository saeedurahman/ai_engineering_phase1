# Week 1 — Module 4 — Practical Assignment 4

**Course:** AI Engineering Foundations  
**Module:** 4 — Structured Outputs & Function Calling (Tool Calling)  
**Status:** ⏳ Pending Student Implementation  

---

## 🎯 Objective
Ek mukammal **Autonomous AI Agent** build karna jo:
1. Customer query ko analyze kare.
2. Khud decide kare ke kya use kisi external database/tool ki zaroorat hai ya nahi.
3. Agar zaroorat ho, toh **Tool Call JSON** generate kare.
4. Hamara Python backend us tool ko execute kare aur live data wapis model ko de.
5. Model us live data ki bunyaad par user ko final polite Roman Urdu response de.
6. Agar tool ki zaroorat na ho, toh normal chat respond kare.

---

## 🛠️ Components
- **Mock Database:** Pakistani Courier Orders (Order 101, 102, 103).
- **Python Tool Function:** `check_order_status(order_id: str) -> dict`.
- **Tool Schema Definition:** OpenAI-compatible function definition.
- **Agent Orchestrator:** Groq API (`qwen/qwen3.8-27b`) tool call loop.

---

## 🧪 Test Scenarios
1. **Live Tool Trigger:** *"Bhai mera order number 102 kahan pohncha hai?"* (Tool call -> In Transit -> Final reply).
2. **Normal Query (No Tool):** *"Aapke store ki timing aur delivery policy kya hai?"* (Direct reply without tool).
3. **Edge Case (Order Not Found):** *"Mera order 999 check karein"* (Tool call -> Not found -> Friendly apology).

---

## ⚙️ Acceptance Criteria
- Correct tool selection by LLM based on description.
- Flawless JSON parsing of tool arguments.
- Two-step API roundtrip (Tool Call -> Tool Output -> Final Answer).
