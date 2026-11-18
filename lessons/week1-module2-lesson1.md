# Week 1 — Module 2 — Lesson 1
## Tokens, Context Window, aur Model Parameters (Temperature, Top-P, Latency)

**Course:** AI Engineering Foundations – From Fundamentals to Production-Ready AI Applications  
**Date:** 2026-11-15  
**Status:** 🔄 In Progress (Lecture Delivered & Knowledge Check Pending)

---

## 🎯 A. Learning Objectives
Is lesson ke baad aap ba-khoobi samjhenge:
1. **Tokens kya hain** aur text kaise numbers (tokens) mein split hota hai (Byte-Pair Encoding).
2. **Input (Prompt) Tokens vs Output (Completion) Tokens** aur inki billing/pricing ka farq.
3. **Context Window** kya hota hai, iski physical limitations kya hain, aur exceed hone par kya hota hai.
4. **Temperature aur Top-P (Nucleus Sampling)** ka mathematically aur practically kya asar hota hai.
5. **Deterministic vs Non-Deterministic Outputs** kab aur kyun zaroori hain.
6. **Max Output Tokens, Model Latency, aur Time To First Token (TTFT)** production metrics.

---

## 🔥 B. Why This Matters (Industry Perspective)
Imagine karein aapne ek AI Legal Assistant ya Medical Chatbot banaya.
- Agar aapne **Temperature = 0.9** rakha, toh AI qanooni daf'aat ya dawaiyon ke formulas mein "creative" ho jayega aur hallucinate karega (jo catastrophic ho sakta hai).
- Agar aapne context window ka hisaab na lagaya, toh 20th message par jaakar user ka puraani baatein bhool jayega ya API crash ho jayegi: `ContextWindowExceededError`.
- Har token par aapka ya aapke client ka paisa lagta hai. Tokenization na samajhne ka matlab hai har mahine hazaron dollars ka be-fizool kharcha!

---

## 📚 C. Main Lecture

---

### 🧩 Part 1: Tokens aur Tokenization Kya Hain?
Computer text ko direct nahi samajhta, aur LLMs bhi pure English ya Urdu ke "words" par kaam nahi karte.

LLMs ke liye text ko **chhotay tukron (chunks)** mein toda jata hai jinhe **Tokens** kehte hain:
- Ek token aam taur par **3 se 4 characters** ya takreeban **0.75 words** ke barabar hota hai (English mein).
- Lekin Roman Urdu, Arabic script, ya code mein ek word ke **zyada tokens** ban sakte hain!

#### Word vs Character vs Subword (BPE - Byte-Pair Encoding)
Aam algorithms text ko subwords mein todte hain. Misal ke taur par:
- Word: `"unbelievable"`
- Tokens ban sakte hain: `["un", "believ", "able"]` (3 tokens)
- Har token ko ek unique **Integer ID** di jati hai (jaise vocabulary dictionary hoti hai).
- Example: `"cat"` = `9246`, `"dog"` = `5679`.

> ⚠️ **Pakistani & International Developer Alert (Roman Urdu Token Cost):**  
> English sentence `"How are you?"` sirf **3 se 4 tokens** leta hai.  
> Lekin Roman Urdu `"Aap kaisay hain?"` shayad **6 se 8 tokens** le, kyunki model ke tokenizer ki vocabulary mein standard English words zyada hote hain aur Roman Urdu syllables toot kar chhotay fragments ban jate hain. Iska matlab Roman Urdu inference thori zyada costly ho sakti hai!

---

### 🧩 Part 2: Input Tokens vs Output Tokens
Har API call mein do qism ke tokens hote hain:

1. **Input Tokens (Prompt Tokens):**
   - Jo text aap model ko bhejte hain (System Prompt + Chat History + User Question).
   - Inhe model sirf "read" karta hai (Parallel processing hoti hai, is liye yeh fast aur cheaper hote hain).

2. **Output Tokens (Completion Tokens):**
   - Jo jawab model generate karta hai.
   - Har naya token pichle token par munhasir hota hai (Autoregressive generation).
   - Yeh sequentially ek ke baad ek bante hain, is liye yeh **slow** aur **zyada mehenge (expensive)** hote hain (aam taur par 2x se 4x mehenge).

---

### 🧩 Part 3: Context Window (Model ki Yaad'dasht ki Hadd)
**Context Window** kisi model ki short-term memory (RAM) hai. Yeh woh maximum tokens ki tadaad hai jo model ek hi waqt mein dekh sakta hai (Input + Output milakar).

| Model | Context Window |
|---|---|
| Llama 3 8B (Base) | 8,192 tokens (~6,000 words) |
| Llama 3.1 / 3.3 70B | 128,000 tokens (~90,000 words) |
| Claude 3.5 Sonnet | 200,000 tokens |
| Gemini 1.5 Pro | 2,000,000 tokens (Books & full videos) |

#### Kya hota hai jab Context Window exceed ho jaye?
1. **Hard Error:** API crash ho jati hai (`Error: context_length_exceeded`).
2. **Context Rot / Amnesia:** Agar aap puraani chat history zabardasti kaat dete hain (Sliding window), toh AI user ki shuruaati shart bhool jata hai.

---

### 🧩 Part 4: Temperature aur Top-P (AI ka Mizaj Control Karna)

Model jab agla token predict karta hai, toh uske paas probabilities hoti hain:
- `"The weather is"` -> `sunny` (60%), `cold` (25%), `rainy` (10%), `banana` (0.0001%)

In probabilities ko filter karne ke do buttons hain:

#### 1. Temperature (Range: 0.0 se 2.0)
- **Temperature = 0.0 (Deterministic / Greedy):**  
  Model hamesha wohi token choose karega jiski probability sab se high hai (60% wala `sunny`). Har dafa same jawab aayega.
  - *Best for:* Coding, JSON output, Math, Medical/Legal facts.
- **Temperature = 0.7 - 0.8 (Balanced):**  
  Normal conversations, blogs, customer support.
- **Temperature = 1.2+ (Wild / Creative):**  
  Poetry, storytelling, brainstorming. Lekin hallucinations ka risk 3x barh jata hai.

#### 2. Top-P (Nucleus Sampling, Range: 0.0 se 1.0)
- Top-P probability mass ka cumulative cutoff hai.
- **Top-P = 0.9:** Iska matlab hai sirf woh top tokens consider karo jinki probabilities milakar 90% banti hain. Baaqi 10% kooda-karkat tokens ko list se bahar phenk do.
- **Top-P = 0.1:** Sirf top 10% highest probability tokens consider honge.

> 💡 **Best Practice Rule:** Temperature aur Top-P dono ko ek sath extreme mat chhero. Ya toh Temperature adjust karo ya Top-P.

---

### 🧩 Part 5: Model Latency & Speed Metrics
Production mein client sirf yeh nahi poochta "jawab sahi hai ya nahi", woh poochta hai "kitni der mein aaya?".

1. **TTFT (Time To First Token):**
   - User ke Send button dabane se le kar pehla lafz screen par aane ka time.
   - Streaming UX ke liye TTFT sab se critical metric hai.
2. **Inference Speed (Tokens Per Second - TPS):**
   - Groq LPUs par: **300 - 800 tokens/sec** (Extreme fast).
   - Standard Cloud GPUs (A100): **40 - 90 tokens/sec**.
   - Local CPU (Ollama): **10 - 25 tokens/sec**.

---

## 🏢 E. Real-World Industry Examples
1. **Clinic Appointment Bot:** Temperature = `0.0`. Agar patient date mangay toh fixed date format de, koi "creative" tareeq na ijaad kare.
2. **E-Commerce JSON API:** Temperature = `0.0`, Max Tokens = `200`. Humein strict JSON chahiye, lambi kahaniyan nahi.
3. **Marketing Copy Generator:** Temperature = `0.85`, Top-P = `0.95`. Naye catchphrases aur marketing lines ke liye creativity zaroori hai.

---

## ⚠️ H. Common Mistakes
1. **Har cheez ke liye default Temperature 1.0 chhor dena:** Nateeja yeh hota hai ke structured JSON crash ho jata hai.
2. **Token vs Word confuse karna:** 1000 words ko 1000 tokens samajh lena (Roman Urdu mein 1000 words aksar 1600+ tokens ban jate hain).
3. **Chat history ko bina pruning ke bhejte rehna:** 10 messages ke baad bill exponential barh jata hai kyunki har turn par pichla sara context dobara Input Tokens ban kar jata hai.
