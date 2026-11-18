# Week 2 — Module 9 — Lesson 1
## Build a Professional AI Chatbot — State Management, Context Sliding Window, Token Cost Auditing & Structured Logging

**Course:** AI Engineering Foundations – From Fundamentals to Production-Ready AI Applications  
**Date:** 2026-11-18  
**Status:** 🔄 In Progress (Lecture Delivered & Knowledge Check Pending)

---

## 🎯 A. Learning Objectives
Is lesson ke baad aap ba-khoobi samjhenge:
1. **Production Chatbot Architecture:** Aik simple 10-line script aur aik modular production application mein structural farq.
2. **Context Window Pruning (Sliding Window Algorithm):** Har message ke sath barhte hue token bill ko control karne ka scientific tareeqa (Linear Cost Growth ko rokna).
3. **Session State Management:** Multi-user conversation history ko isolate rakhna taake Customer A ki baat Customer B ke context mein leak na ho.
4. **Live Token & Cost Auditing:** Har chat session ke aakhir mein exact dollar cost calculate karke user ya analytics ko dikhana.
5. **Structured Audit Logging (JSONL / File Logger):** Future debugging aur model evaluation ke liye tamam conversations ko audit trail mein persist karna.
6. **Clean Directory & Module Structure:** Config, Core Client, Bot Logic, aur Utilities ko alag alag rakhna.

---

## 🔥 B. Why This Matters (Production Engineering Perspective)
Junior developer ka chatbot:
- Saari history ek hi global list mein append karta rehta hai.
- 15 messages ke baad model context window overflow ho jati hai ya API bill 10x ho jata hai.
- Agar server restart ho jaye, toh saara conversation data ghayab ho jata hai.
- Company ko pata hi nahi chalta ke user ne kya baat ki aur kitna paisa kharch hua.

Senior AI Engineer ka chatbot:
- **Sliding Window** use karta hai: Hamesha System Prompt ko protect karta hai aur sirf aakhri $N$ messages (e.g. last 6 messages) bhejta hai taake cost flat rahe.
- **Audit Logging** maintain karta hai: Har prompt aur response JSONL file mein timestamp ke sath save hota hai.
- **Cost Telemetry** deta hai: Dashboard par foran dikhata hai: *"This session consumed 450 tokens ($0.000045)"*.

---

## 📚 C. Main Lecture

---

### 🧩 Part 1: The Context Sliding Window Algorithm

Aapko yaad hai Module 6 mein humne discuss kiya tha ke har naye turn par pichla poora conversation dobara tokenize hota hai?

Agar hum bina limit ke append karte rahein:
```
Turn 1: [System, Msg1] -> 200 tokens
Turn 10: [System, Msg1, Msg2, ... Msg20] -> 2,500 tokens
Turn 30: [System, Msg1, ... Msg60] -> 8,000 tokens (Context Window Crash & Heavy Bill!)
```

#### Sliding Window Solution:
Hum System Prompt (Constitutional Rules) ko **hamesha index 0** par locked rakhte hain, aur baaqi messages ki list ko sirf aakhri $K$ turns (e.g., 6 messages = 3 user + 3 assistant) par slice kar dete hain:

```python
def get_pruned_messages(
    history: List[dict], max_messages: int = 6
) -> List[dict]:
    # System prompt hamesha zaroori hai
    system_prompt = history[0]

    # Baaqi messages mein se sirf aakhri N messages uthao
    recent_messages = history[1:][-max_messages:]

    return [system_prompt] + recent_messages
```
**Faida:** Chahe customer 100 messages kare, model ke paas hamesha sirf 6 recent messages jayenge — **Context kabhi crash nahi hoga aur bill hamesha flat aur predictable rahega!**

---

### 🧩 Part 2: Session State Management

Real-world web APIs (FastAPI, Next.js, Flutter Backend) mein ek hi server par 100 users baatein kar rahe hote hain:
- Agar aap global variable `history = []` use karenge, toh Ali ka message Sara ke context mein mix ho jayega (Critical Data Privacy Leak!).
- Is liye hum **Session IDs** (jaise `session_abc123`) use karte hain, aur har session ki apni alag memory dictionary maintain hoti hai:
  ```python
  sessions: Dict[str, List[dict]] = {
      "user_ali_101": [{"role": "system", ...}, ...],
      "user_sara_202": [{"role": "system", ...}, ...],
  }
```

---

### 🧩 Part 3: Structured Conversation Logging (Audit Trail)

Production mein AI kya bol raha hai, yeh monitor karna qanooni aur technical dono lehaaz se zaroori hai.

Hum har conversation turn ko **JSON Lines (`conversations.jsonl`)** format mein append karte hain:
```json
{"timestamp": "2026-11-18T08:50:00", "session_id": "sess_01", "provider": "groq", "user": "Delivery charges kitne hain?", "assistant": "Rs 200 flat across Pakistan.", "tokens": 128, "cost_usd": 0.000012}
```
Is file se analytics bante hain, customer disputes resolve hote hain, aur future mein model fine-tuning ke liye data milta hai.

---

### 🧩 Part 4: Clean Modular Project Structure

Production AI projects mein code is tarah divide hota hai:

```text
phase1-2/
│
├── config.py             # System Prompts, Models, Token Pricing
├── client.py             # Unified AI Client (Groq + Ollama + Failover)
├── chatbot.py            # Chatbot class (State, Sliding Window, Logging)
└── run_chatbot.py        # Terminal / CLI interactive interface
```

---

## 🏢 E. Real-World Business Examples
1. **Daraz / E-Commerce Support:** Lakhon customers ke chats chal rahe hote hain. Sliding Window na ho toh server 10 minute mein out-of-memory ho jaye.
2. **Medical Clinic Consultation:** Doctor review ke liye har chat ka JSONL audit log save hota hai taake verify kiya ja sake ke bot ne koi galat dawai recommend nahi ki.

---

## ⚠️ H. Common Mistakes
1. Sliding window karte waqt **System Prompt ko bhi drop kar dena** (Jis se bot persona aur company rules bhool jata hai).
2. Streaming ke doran token count measure na karna.
3. Multi-user state ko global list mein rakh kar user data cross-contaminate kar dena.

---

## 📝 J. Lesson Summary
- **Sliding Window:** System Prompt + Last $N$ messages = Flat cost & zero context overflow.
- **State Isolation:** Session ID based chat storage.
- **Audit Logging:** Har turn ko JSONL format mein persist karna.
- **Telemetry:** Live tokens aur cost tracking per user.
