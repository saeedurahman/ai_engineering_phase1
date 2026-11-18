from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ModelPricing:
    name: str
    provider: str
    input_cost_per_1m: float  # $ per 1,000,000 input tokens
    output_cost_per_1m: float  # $ per 1,000,000 output tokens


# =====================================================================
# 📊 INDUSTRY PRICING CATALOG (Official Rates per 1M Tokens)
# =====================================================================
MODELS_CATALOG: List[ModelPricing] = [
    ModelPricing("Llama 3.1 8B", "Groq Cloud", 0.05, 0.08),
    ModelPricing("Qwen 2.5 72B", "Groq Cloud", 0.59, 0.79),
    ModelPricing("GPT-4o", "OpenAI", 2.50, 10.00),
    ModelPricing("Claude 3.5 Sonnet", "Anthropic", 3.00, 15.00),
    ModelPricing("Local Llama (Ollama)", "On-Premise", 0.00, 0.00),
]


def calculate_saas_unit_economics(
    active_users: int = 500,
    chats_per_user_per_month: int = 15,
    turns_per_chat: int = 4,
    avg_input_tokens_per_turn: int = 400,
    avg_output_tokens_per_turn: int = 120,
    monthly_subscription_price_usd: float = 12.00,
):
    """Calculates comprehensive financial and token economics across multiple AI models."""

    # 1. Total Usage Calculations
    total_chats_per_month = active_users * chats_per_user_per_month
    total_turns_per_month = total_chats_per_month * turns_per_chat

    # Token Volume (in Millions)
    total_input_tokens = total_turns_per_month * avg_input_tokens_per_turn
    total_output_tokens = total_turns_per_month * avg_output_tokens_per_turn

    total_input_millions = total_input_tokens / 1_000_000
    total_output_millions = total_output_tokens / 1_000_000

    # Total Monthly Revenue
    monthly_revenue = active_users * monthly_subscription_price_usd

    print("=" * 80)
    print("💼 AI SAAS UNIT ECONOMICS & PROFITABILITY CALCULATOR")
    print("=" * 80)
    print(f"👥 Monthly Active Users:        {active_users:,}")
    print(
        f"💬 Monthly Total Conversations:  {total_chats_per_month:,} ({chats_per_user_per_month} chats/user)"
    )
    print(
        f"🔄 Monthly Total Turns (Msgs):  {total_turns_per_month:,} ({turns_per_chat} turns/chat)"
    )
    print(
        f"📥 Monthly Input Tokens:        {total_input_tokens:,} ({total_input_millions:.2f} Million)"
    )
    print(
        f"📤 Monthly Output Tokens:       {total_output_tokens:,} ({total_output_millions:.2f} Million)"
    )
    print(
        f"💵 Monthly Subscription Fee:    ${monthly_subscription_price_usd:.2f} per user"
    )
    print(f"💰 Total Monthly Revenue:       ${monthly_revenue:,.2f}")
    print("=" * 80)

    print(
        f"\n{'Model Name':<20} | {'Monthly Bill':<12} | {'Cost/User':<10} | {'Cost/1k Chats':<13} | {'Gross Profit':<12} | {'Margin (%)':<10}"
    )
    print("-" * 88)

    for model in MODELS_CATALOG:
        # Cost Formula
        input_bill = total_input_millions * model.input_cost_per_1m
        output_bill = total_output_millions * model.output_cost_per_1m
        total_monthly_bill = input_bill + output_bill

        cost_per_user = total_monthly_bill / active_users
        cost_per_1k_chats = (
            total_monthly_bill / (total_chats_per_month / 1000)
            if total_chats_per_month > 0
            else 0
        )

        gross_profit = monthly_revenue - total_monthly_bill
        profit_margin = (
            (gross_profit / monthly_revenue) * 100 if monthly_revenue > 0 else 0
        )

        print(
            f"{model.name:<20} | ${total_monthly_bill:>10.2f} | ${cost_per_user:>8.3f} | ${cost_per_1k_chats:>11.2f} | ${gross_profit:>10.2f} | {profit_margin:>8.1f}%"
        )

    print("-" * 88)
    print("\n💡 SENIOR AI ARCHITECT RECOMMENDATION:")
    print("1. Routine Customer Support / Classification ke liye Llama 3.1 8B (Groq) use karein (99.8% Margin!).")
    print(
        "2. Complex Reasoning ke liye Qwen 2.5 72B use karein (98.3% Margin!)."
    )
    print(
        "3. GPT-4o / Claude 3.5 ko sirf critical coding ya multi-modal tasks ke liye reserve rakhein taake bill safe rahe."
    )
    print("=" * 80)


if __name__ == "__main__":
    calculate_saas_unit_economics(
        active_users=500,  # 500 Paying Customers
        chats_per_user_per_month=15,  # Har user mahine mein 15 chats karta hai
        turns_per_chat=4,  # Har chat 4 messages ki hoti hai
        avg_input_tokens_per_turn=400,  # History samait input tokens
        avg_output_tokens_per_turn=120,  # AI ka response
        monthly_subscription_price_usd=15.00,  # SaaS charge: $15/month
    )