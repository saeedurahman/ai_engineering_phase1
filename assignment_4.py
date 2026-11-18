import json
import os
import time
from typing import Any, Dict
from dotenv import load_dotenv
from groq import Groq


def get_groq_client() -> Groq:
    """Loads environment and initializes Groq client."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY nahi mili! .env file check karein.")
    return Groq(api_key=api_key)


# =====================================================================
# 📦 STEP 1: MOCK DATABASE & REAL PYTHON TOOL
# =====================================================================
ORDERS_DATABASE: Dict[str, Dict[str, Any]] = {
    "101": {
        "customer": "Ali Khan",
        "item": "Embroidered Kurta",
        "status": "DELIVERED",
        "city": "Karachi",
        "delivered_on": "14 Nov 2026",
    },
    "102": {
        "customer": "Sara Ahmed",
        "item": "Lawn 3-Piece Suit",
        "status": "IN_TRANSIT",
        "city": "Lahore",
        "courier": "TCS Express",
        "rider_name": "Hamza",
        "expected_delivery": "Today by 5:00 PM",
    },
    "103": {
        "customer": "Usman Tariq",
        "item": "Leather Jacket",
        "status": "PROCESSING",
        "city": "Islamabad",
        "notes": "Quality check in progress at warehouse",
    },
}


def check_order_status(order_id: str) -> str:
    """Real Python function jo database se order check karta hai."""
    print(
        f"\n⚙️ [PYTHON BACKEND EXECUTING]: check_order_status(order_id='{order_id}')"
    )

    clean_id = str(order_id).strip()
    if clean_id in ORDERS_DATABASE:
        data = ORDERS_DATABASE[clean_id]
        return json.dumps({"found": True, "order_id": clean_id, **data})
    else:
        return json.dumps(
            {
                "found": False,
                "order_id": clean_id,
                "error": "Order ID database mein mojood nahi hai.",
            }
        )


# =====================================================================
# 🛠️ STEP 2: TOOL SCHEMA (AI KO TOOLS KA MENU DIKHANA)
# =====================================================================
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": "Checks real-time tracking, courier, and shipping status of a customer order using the numeric Order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The numeric order ID, e.g., '101', '102'.",
                    }
                },
                "required": ["order_id"],
            },
        },
    }
]

SYSTEM_PROMPT = """
You are 'Ayesha', a helpful customer support agent for PakStyle Apparel.
Speak in polite, professional Roman Urdu.
If a customer asks about their order status or tracking, USE the check_order_status tool.
Once the tool returns the data, explain the status clearly and kindly to the customer.
If the customer asks general questions not related to specific orders, answer directly without using tools.
"""


# =====================================================================
# 🔄 STEP 3: FUNCTION CALLING ORCHESTRATION LOOP
# =====================================================================
def run_autonomous_agent(client: Groq, user_query: str):
    """Executes the complete 5-step Function Calling cycle."""
    model_name = "qwen/qwen3.8-27b"

    print("\n" + "=" * 75)
    print(f"👤 CUSTOMER QUERY: \"{user_query}\"")
    print("=" * 75)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ]

    # 1. Pehli API Call: max_tokens=150 set kiya taake rate limit na aaye
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto",
        temperature=0.0,
        max_tokens=150,  # 👈 Token limit protect kar rahi hai
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # 2. Check: Kya Model ne Tool Call karne ka faisla kiya?
    if tool_calls:
        print("🧠 [AI DECISION]: External Tool ki zaroorat hai!")
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            raw_args = tool_call.function.arguments
            parsed_args = json.loads(raw_args)

            print(
                f"📝 [AI GENERATED PARCHI]: Tool={function_name} | Args={parsed_args}"
            )

            # 3. Python Execution: Real Python function run karte hain
            if function_name == "check_order_status":
                tool_output = check_order_status(
                    order_id=str(parsed_args.get("order_id"))
                )
                print(f"📡 [DATABASE OUTPUT]: {tool_output}")

                # 4. Result wapas AI ko bhejte hain
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": tool_output,
                    }
                )

        # 5. Doosri API Call: Model tool result parh kar final human response dega
        second_response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.3,
            max_tokens=200,  # 👈 Token limit
        )
        final_reply = second_response.choices[0].message.content.strip()
        print(f"\n👩‍💼 AYESHA (FINAL REPLY): \n{final_reply}")

    else:
        # Agar tool ki zaroorat nahi thi (Direct Chat)
        print("🧠 [AI DECISION]: Kisi tool ki zaroorat nahi hai (Direct Chat).")
        print(f"\n👩‍💼 AYESHA (DIRECT REPLY): \n{response_message.content.strip()}")


if __name__ == "__main__":
    client = get_groq_client()

    # Scenario 1: Tool Call Required (Live Tracking)
    run_autonomous_agent(
        client, "Assalam o Alaikum, mera order number 102 kahan pohncha hai?"
    )

    time.sleep(2)  # Rate limit cooldown

    # Scenario 2: Direct Chat (No Tool Needed)
    run_autonomous_agent(
        client, "Aapke paas Cash on Delivery available hai ya nahi?"
    )

    time.sleep(2)  # Rate limit cooldown

    # Scenario 3: Tool Call for Invalid ID (Edge Case)
    run_autonomous_agent(client, "Bhai zara order 999 ka status batana.")