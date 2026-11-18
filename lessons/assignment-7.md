# Week 1 — Module 7 — Practical Assignment 7

**Course:** AI Engineering Foundations  
**Module:** 7 — API Cost Engineering & SaaS Profitability Calculator  
**Status:** ⏳ Pending Student Implementation  

---

## 🎯 Objective
Ek comprehensive Python application build karna jo:
1. Industry ke popular cloud models (`Llama 3.1 8B`, `Qwen 2.5 72B`, `GPT-4o`, `Claude 3.5 Sonnet`, aur `Local Ollama`) ki token pricing ka comparative hisaab lagaye.
2. Real-world SaaS metrics calculate kare:
   - Cost per Conversation
   - Cost per User per Month
   - Cost per 1,000 Conversations
   - Total Monthly API Bill
   - SaaS Revenue, Gross Profit ($), aur Profit Margin (%)
3. Side-by-side financial comparison report print kare taake software founders accurate business decisions le sakein.

---

## 🛠️ Pricing Catalog (Per 1 Million Tokens)
- **Llama 3.1 8B (Groq):** Input = $0.05 | Output = $0.08
- **Qwen 2.5 72B (Groq):** Input = $0.59 | Output = $0.79
- **GPT-4o (OpenAI):** Input = $2.50 | Output = $10.00
- **Claude 3.5 Sonnet:** Input = $3.00 | Output = $15.00
- **Local Ollama:** Input = $0.00 | Output = $0.00

---

## ⚙️ Acceptance Criteria
- Clean, typed, modular Python script (`assignment_7.py`).
- Flawless token math based on actual turn accumulation.
- Clear financial comparison table printed to the terminal.
