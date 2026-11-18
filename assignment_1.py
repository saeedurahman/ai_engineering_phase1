import os
from typing import Dict, List
from dotenv import load_dotenv


def verify_environment() -> bool:
    """Securely checks if required environment variables are loaded."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or api_key == "your_groq_api_key_here":
        print("❌ ERROR: GROQ_API_KEY nahi mili ya invalid hai!")
        return False

    masked_key = f"{api_key[:6]}...{api_key[-4:]}"
    print(f"✅ Environment Verified! Groq API Key loaded: {masked_key}\n")
    return True


def rule_based_classifier(user_query: str) -> str:
    """Traditional Rule-Based Classifier using keyword matching."""
    query_lower = user_query.lower()

    # Keyword rules for Pakistani E-Commerce Support
    order_keywords = ["order", "track", "kahan hai", "status"]
    sales_keywords = ["kharidna", "price", "kitne ka", "kitnay ka", "rate"]
    complaint_keywords = ["kharaab", "wapis", "fault", "defect", "tuta"]

    # Simple matching logic
    for kw in order_keywords:
        if kw in query_lower:
            return "ORDER_TRACKING"

    for kw in sales_keywords:
        if kw in query_lower:
            return "SALES_INQUIRY"

    for kw in complaint_keywords:
        if kw in query_lower:
            return "COMPLAINT"

    return "UNKNOWN"


def run_experiment():
    """Runs test cases against rule-based system to observe fragility."""

    # Test cases: Roman Urdu customer queries with expected human intent
    test_cases: List[Dict[str, str]] = [
        {
            "query": "Yeh suit kitnay ka hai aur delivery charges kya hain?",
            "expected": "SALES_INQUIRY",
            "reason": "Direct keyword 'kitnay ka' mojood hai.",
        },
        {
            "query": "Bhai mera parcel abhi tak nahi pohncha, 5 din ho gaye!",
            "expected": "ORDER_TRACKING",
            "reason": "Customer tracking chahta hai, lekin 'order' ya 'track' ka lafz nahi bola ('parcel' bola).",
        },
        {
            "query": "Mujhe cheez pasand nahi aayi, tabdeel karwana hai.",
            "expected": "COMPLAINT",
            "reason": "Customer exchange chahta hai, lekin 'wapis' ya 'kharaab' nahi bola ('tabdeel' bola).",
        },
        {
            "query": "Koi sunne wala hai yahan ya sab so rahe hain?",
            "expected": "COMPLAINT",
            "reason": "Gusse aur frustration ka izhar hai, lekin koi direct keyword nahi hai.",
        },
    ]

    print("=" * 70)
    print("🤖 TRADITIONAL RULE-BASED SYSTEM VS HUMAN LANGUAGE TEST")
    print("=" * 70)

    passed_count = 0

    for i, test in enumerate(test_cases, start=1):
        query = test["query"]
        expected = test["expected"]
        predicted = rule_based_classifier(query)

        is_match = predicted == expected
        if is_match:
            passed_count += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL (Semantic Miss)"

        print(f"\n[Test {i}] Query: '{query}'")
        print(f"  👉 Expected Intent: {expected}")
        print(f"  👉 Rule Predicted:  {predicted} -> {status}")
        print(f"  💡 Why it matters:  {test['reason']}")

    print("\n" + "=" * 70)
    print(f"📊 RESULT SUMMARY: {passed_count}/{len(test_cases)} Passed")
    print("=" * 70)
    print("💡 CONCLUSION:")
    print("Traditional programming tab fail hoti hai jab human expressions")
    print("aur synonyms badal jayein. Isi liye humein aglay module mein")
    print("AI / LLMs ki zaroorat parti hai jo 'meaning (semantics)' samajhte hain!")


if __name__ == "__main__":
    if verify_environment():
        run_experiment()