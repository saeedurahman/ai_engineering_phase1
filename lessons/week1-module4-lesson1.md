# Week 1 — Module 4 — Lesson 1
## Structured Outputs aur Function Calling — JSON Schemas, Pydantic, aur AI Tools Execution

**Course:** AI Engineering Foundations – From Fundamentals to Production-Ready AI Applications  
**Date:** 2026-11-16  
**Status:** 🔄 In Progress (Lecture Delivered & Knowledge Check Pending)

---

## 🎯 A. Learning Objectives
Is lesson ke baad aap ba-khoobi samjhenge:
1. **Structured Output kya hai** aur software engineering mein plain text ke muqablay mein JSON kyun zaroori hai.
2. **JSON Schema aur Pydantic Models:** Python types ke zariye AI response ko 100% strictly type-safe kaise banaya jata hai.
3. **Function Calling (Tool Calling) ka Asal Falsafa:** AI khud Python function run **nahi** karta, balke execute karne ka decision aur parameters provide karta hai.
4. **LLM Tool Selection Logic:** Model kaise decide karta hai ke kab aam baat karni hai aur kab koi tool (jaise `check_order_status` ya `send_sms`) trigger karna hai.
5. **Execution Loop & Error Handling:** Application kaise AI ke generated JSON parameters ko le kar real Python function chalati hai aur result wapis AI ko deti hai.

---

## 🔥 B. Why This Matters (Production Engineering Perspective)
Agar aap Flutter ya Next.js developer hain, toh aap jante hain ke aapka frontend ya database plain English paragraph nahi parh sakta:
- Agar AI kahe: *"Ji aapka order #12345 Karachi se nikal chuka hai aur 2 din mein milega"* — toh Flutter app is par screen kaise draw karegi?
- Lekin agar AI de:
  ```json
  {"status": "IN_TRANSIT", "order_id": 12345, "estimated_days": 2}
  ```
  Toh aapki Flutter app foran ek khoobsurat Progress Bar aur Tracking Badge render kar sakti hai!

**Structured Outputs** aur **Function Calling** hi woh cheez hain jo ek "Chatbot" ko ek **Autonomous AI Agent** mein badalti hain!

---

## 📚 C. Main Lecture

---

### 🧩 Part 1: Plain Text vs Structured Output (JSON)

Traditional software mein data flows via APIs:
```
Frontend (Flutter / Next.js)  <-- JSON -->  Backend (Python / Node)  <-- SQL --> Database
```

Jab hum LLM ko software architecture ke darmian lagate hain, toh agar woh markdown ya be-tarteeb text dega, toh `json.loads()` crash ho jayega:  
`json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes`

**Structured Output** ka matlab yeh guarantee lena hai ke AI ka response **hamesha valid JSON** hoga jo hamare tay-shuda Schema ko follow karega.

---

### 🧩 Part 2: Pydantic — The AI Engineer’s Best Friend

Python mein data validation ke liye industry standard library hai **Pydantic**.  
Pydantic se hum define karte hain ke humein kaisa data chahiye:

```python
from pydantic import BaseModel, Field
from typing import Literal


class OrderClassification(BaseModel):
    intent: Literal["TRACKING", "SALES", "COMPLAINT", "GENERAL"]
    confidence_score: float = Field(
        description="Confidence between 0.0 and 1.0"
    )
    extracted_order_id: int | None = Field(
        default=None, description="5-digit order id if found in query"
    )
    reply_to_customer: str = Field(description="Polite Roman Urdu reply")
```

Jab hum yeh schema model ko dete hain, toh model kisi doosre format mein jawab de hi nahi sakta!

---

### 🧩 Part 3: Function Calling (Tool Calling) Kya Hai?

Yeh AI Engineering ka **sab se ahem concept** hai.

> ⚠️ **Misconception:** Bohat se developers samajhte hain ke LLM hamara Python function ya SQL database direct access karta hai.  
> **Haqeeqat:** LLM sirf aik **Brain (Faisla-saz)** hai, uske haath paon nahi hote!

#### Step-by-Step Function Calling Workflow:

```
[1. User Query] 
      │ "Mera order 54321 kahan hai?"
      ▼
[2. App sends prompt + Tool Definitions to Groq]
      │ Tools: [check_order_status(order_id: int)]
      ▼
[3. LLM Decides & Generates Tool Call Arguments]
      │ "Mujhe check_order_status chalana chahiye with order_id=54321"
      ▼ (API returns tool_calls JSON)
[4. Hamari Python App executes the REAL Python function]
      │ def check_order_status(54321): ... DB query ...
      │ Result: {"status": "Dispatched from Lahore"}
      ▼
[5. App sends Tool Result BACK to LLM]
      │
      ▼
[6. LLM generates final natural language reply to user]
      │ "Aapka order Lahore se nikal chuka hai!"
```

---

### 🧩 Part 4: OpenAI-Compatible Tool Schema

Groq aur OpenAI mein tools is tarah define hote hain:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "track_order",
            "description": "Checks the real-time shipping status of a customer order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The 5-digit order tracking number, e.g. '12345'",
                    }
                },
                "required": ["order_id"],
            },
        },
    }
]
```

Model is `description` ko parh kar khud samajhta hai ke user ki baat sun kar yeh tool chalana hai ya nahi!

---

## 🏢 E. Real-World Business Examples
1. **Hospital Appointment Bot:**  
   User: *"Mujhe kal subha 10 baje Dr. Imran ke sath appointment book karni hai."*  
   LLM tool call karega: `book_appointment(doctor="Dr. Imran", date="2026-11-17", time="10:00")`.  
   Aapka Python code hospital database mein appointment save karega.
2. **Shopify / E-Commerce Assistant:**  
   User: *"Kya blue colour mein medium size shirt available hai?"*  
   LLM tool call karega: `check_inventory(sku="SHIRT-BLU-M")`.

---

## ⚠️ H. Common Mistakes
1. **JSON parsing try/except ke baghair karna:** AI kabhi kabhi JSON ke ird gird ```json ... ``` laga deta hai agar prompt sahi na ho.
2. **LLM ko private credentials dena:** Function definition mein database passwords kabhi nahi bhejne, sirf function ka naam aur parameters bhejne hain.
3. **Tool Execution fail hone par crash hona:** Agar database down ho, toh error ko gracefully handle karke AI ko batana chahiye taake woh customer se maazrat kare.

---

## 📝 J. Lesson Summary
- **Structured Output (JSON):** Software APIs ke sath baat karne ke liye lazmi hai.
- **Pydantic:** Schema validation aur type safety provide karta hai.
- **Function Calling:** LLM faisla karta hai aur arguments generate karta hai; Python application function ko physically execute karti hai.
