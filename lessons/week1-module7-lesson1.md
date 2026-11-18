# Week 1 — Module 7 — Lesson 1
## API Cost Engineering — Token Pricing Math, Monthly Budget Estimation, Model Comparison & SaaS Profitability

**Course:** AI Engineering Foundations – From Fundamentals to Production-Ready AI Applications  
**Date:** 2026-11-18  
**Status:** 🔄 In Progress (Lecture Delivered & Knowledge Check Pending)

---

## 🎯 A. Learning Objectives
Is lesson ke baad aap ba-khoobi samjhenge:
1. **Token Pricing Unit:** $ per 1 Million (1M) tokens ka standard hisaab kitab.
2. **Input vs Output vs Cached Token Pricing:** Output tokens 3x se 4x mehenge kyun hote hain aur Prompt Caching se 80% bachat kaise hoti hai.
3. **Unit Economics Formula:** Cost per Request -> Cost per Conversation -> Cost per Active User -> Monthly Cloud Bill.
4. **Cloud vs Local Hardware Cost Tradeoff:** Cloud API bill vs on-premise GPU server (electricity + hardware depreciation).
5. **SaaS Pricing & Profit Margins:** AI features ka subscription rate kaise tay karein taake 70%+ gross profit margin bache.
6. **Cost Kill-Switches & Hard Limits:** Unexpected $10,000 credit card bills se bachne ke production tools.

---

## 🔥 B. Why This Matters (The Business of AI Engineering)
Dunya mein 80% AI startups is liye fail ho jate hain kyunki developers code likhna toh seekh jate hain, lekin **Unit Economics (Paisa aur Munafa)** ka hisaab nahi lagate!

Imagine karein:
- Aapne Next.js par ek AI Document Summarizer SaaS banaya.
- Aapne subscription fee rakhi: **$10 per month**.
- Ek heavy user ne har roz 50 lambi PDF files summarize karwa li.
- Month ke aakhir mein pata chala ke us user ki vajah se OpenAI ka bill **$45** ban gaya!
- **Nateeja:** Har user par aapko **$35 ka nuqsan (loss)** hua! Jitne zyada users aayenge, company utni tezi se deewalia (bankrupt) hogi!

Aik **Senior AI Engineer** hamesha pehle excel sheet ya Python calculator par token math calculate karta hai, model optimize karta hai, aur phir aisa software banata hai jo **80% Profit Margin** generate kare!

---

## 📚 C. Main Lecture

---

### 🧩 Part 1: Token Pricing Standard ($ / 1 Million Tokens)

Industry mein tamam providers (OpenAI, Anthropic, Groq, DeepSeek, Google) apni pricing **Per 1 Million (1,000,000) Tokens** mein quote karte hain.

Misal ke taur par (Standard Market Rates):

| Model | Input Cost / 1M Tokens | Output Cost / 1M Tokens | Speed & Best Use Case |
|---|---|---|---|
| **Llama 3.1 8B (Groq)** | **$0.05** (Sirf 5 Cents) | **$0.08** (Sirf 8 Cents) | Extreme Fast, Ultra Cheap, Classification |
| **Qwen 2.5 72B (Groq)**| **$0.59** | **$0.79** | Smart Reasoning, Multi-turn Chat |
| **GPT-4o (OpenAI)** | **$2.50** | **$10.00** | High Intelligence, Vision, Complex Logic |
| **Claude 3.5 Sonnet** | **$3.00** | **$15.00** | Best Coding & Agentic Workflows |

> 💡 **Notice the Gap:** GPT-4o output token Llama-8B se **125 Guna Mehenga** hai! Agar aap simple customer support classification ke liye GPT-4o use karenge, toh aap client ka paisa aag mein jala rahe hain!

---

### 🧩 Part 2: Unit Economics Formula (Kharche Ka Hisaab)

AI app ka kharcha calculate karne ke 4 ahem steps hote hain:

#### 1. Cost Per Single Request Formula:
$$\text{Cost} = \left(\frac{\text{Input Tokens}}{1,000,000} \times \text{Input Price}\right) + \left(\frac{\text{Output Tokens}}{1,000,000} \times \text{Output Price}\right)$$

#### 2. Cost Per Conversation (Turn Math):
Socho ek aam E-Commerce customer support chat mein:
- Average **5 turns (questions/answers)** hote hain.
- Har turn par chat history accumulate hoti hai (jo humne Module 5 mein dekha):
  - Turn 1: 150 input, 100 output
  - Turn 2: 350 input, 100 output
  - Turn 3: 550 input, 100 output
  - Turn 4: 750 input, 100 output
  - Turn 5: 950 input, 100 output
- **Total per conversation:** ~2,750 Input Tokens aur 500 Output Tokens.

#### 3. Monthly Bill for 1,000 Daily Customers (30,000 chats/month):
- **Using Llama-3.1-8B on Groq:**  
  Input: $\frac{30,000 \times 2,750}{1M} \times \$0.05 = \$4.12$  
  Output: $\frac{30,000 \times 500}{1M} \times \$0.08 = \$1.20$  
  👉 **Total Month Bill = Sirf $5.32 (Takreeban Rs 1,500/month)!**

- **Using GPT-4o:**  
  Input: $\frac{82.5M}{1M} \times \$2.50 = \$206.25$  
  Output: $\frac{15M}{1M} \times \$10.00 = \$150.00$  
  👉 **Total Month Bill = $356.25 (Takreeban Rs 100,000/month)!**

---

### 🧩 Part 3: Prompt Caching (The 80% Discount Weapon)

Modern providers (Anthropic, DeepSeek, OpenAI) ne **Prompt Caching** introduce kiya hai:
- Agar aapka System Prompt bara hai (e.g. 2,000 tokens of company documents/policies), aur har customer wohi bar bar parhta hai:
- Server pehli dafa full price leta hai, lekin uske baad har request par **75% se 90% discount** deta hai!
- **Cached Input Tokens:** $2.50 ke bajaye sirf **$0.30 / 1M** lagta hai!

---

### 🧩 Part 4: SaaS Pricing & Profit Margins (How to Make Money 💵)

Jab aap client ko SaaS ya AI automation solution bechte hain, toh **The Rule of 3x-5x** use karein:

1. **Calculate Maximum Expected Cost per User:**  
   Agar ek typical active customer mahine mein **$2.00** ki API tokens consume karta hai.
2. **Add Infrastructure & Buffer (20%):**  
   Server hosting (Vercel/AWS) + Database = $0.50. Total COGS = $2.50.
3. **Set Subscription Price for 70%+ Margin:**  
   $$\text{Price} = \text{COGS} \times 4 = \$2.50 \times 4 = \$10.00 / \text{month}$$
   - $10.00 revenue - $2.50 cost = **$7.50 Net Gross Profit (75% Profit Margin)!**

---

### 🧩 Part 5: Production Cost Protection (Kill-Switches)

Har professional developer ko yeh 3 safety checks lagane chahiye:
1. **Hard Spend Limits (Provider Dashboard):** Groq aur OpenAI dashboard par monthly spend cap set karein (e.g. $50). Is se upar card charge hi nahi hoga.
2. **User Rate Limiting:** Ek user ko 1 ghante mein max 20 messages ki limit dein taake koi bot aapka account khali na kar sake.
3. **`max_tokens` Guard:** Har completion call mein strict `max_tokens` lazmi dein taake runaway generation na ho.

---

## 🏢 E. Real-World Business Examples
1. **Pakistani School Management SaaS:**  
   100 schools ke liye report card generator. Llama-3-8B use karke pure saal ka API bill sirf $30 banta hai, jabke SaaS school se $500 charge karta hai (94% Profit!).
2. **Medical Clinic Chatbot:**  
   Local Ollama chala kar API bill $0 kar diya, client se $150/month maintenance fee li (100% Margin!).

---

## ⚠️ H. Common Mistakes
1. Pricing ko "Per 1,000 tokens" samajhna (Aaj kal pricing **Per 1 Million tokens** hoti hai).
2. Input aur Output tokens ka same rate samajhna (Output 3x mehenga hota hai).
3. Chat history ke token accumulation ka hisaab na lagana.
4. Bina spending limit set kiye live production release kar dena.

---

## 📝 J. Lesson Summary
- **Pricing Standard:** Always calculate in $ / 1M tokens.
- **Output Tokens:** Sequential generation ki vajah se 3x-4x zyada mehenge hote hain.
- **Model Routing:** Routing easy tasks to 8B models saves 90% cloud cost.
- **SaaS Margin:** Target at least 70% gross profit margin after token costs.
