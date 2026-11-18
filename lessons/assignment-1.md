# Week 1 — Module 1 — Practical Assignment 1

**Course:** AI Engineering Foundations  
**Module:** 1 — Introduction to AI & LLMs  
**Status:** ⏳ Pending Student Submission  

---

## 🎯 Objective
1. Setup production-grade Python environment (Virtual Environment + Secure `.env` handling).
2. Practically demonstrate why Traditional Rule-Based Programming fails for Natural Language and why AI / LLMs are required.

---

## 📋 Tasks

### Part 1: Secure Environment Setup
- Virtual Environment create karein (`.venv`).
- Packages install karein: `python-dotenv`, `groq`.
- `.env` file create karein: `GROQ_API_KEY=your_key_here`.
- `.gitignore` create karein jo `.env` aur `.venv` ko ignore kare.
- Python mein safely verify karein ke key exist karti hai (print na karein).

### Part 2: Rule-Based Fragility Demonstration
- Function: `rule_based_classifier(user_query: str) -> str`
- Intent classes: `ORDER_TRACKING`, `SALES_INQUIRY`, `COMPLAINT`, `UNKNOWN`
- Test with varied Roman Urdu customer queries.
- Demonstrate why human language nuances break static keyword rules.

---

## ⚙️ Acceptance Criteria
- PEP 8 compliant code with type hints.
- Zero hardcoded secrets.
- Clear console output highlighting rule-based failures on edge cases.
