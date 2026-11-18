from datetime import datetime
import json
import os
import time
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI


# =====================================================================
# ⚙️ SYSTEM PROMPT & STORE KNOWLEDGE
# =====================================================================
SYSTEM_PROMPT = """
You are "Ayesha", Senior Customer Support Executive for "PakStyle Apparel", a premium clothing brand.
You speak polite, friendly, and natural Pakistani Roman Urdu (or English if the customer asks in English).

STORE POLICIES:
- Delivery: Rs 200 flat across Pakistan. Free delivery on orders above Rs 3,000.
- Return & Exchange: 7 days window. Must have original tags and be unwashed.
- Max Discount: 10% coupon code SAVE10 for orders above Rs 5,000. Never offer more than 10%.
Keep your responses helpful, concise, and professional.
"""


class ProductionBusinessChatbot:

    def __init__(
        self,
        provider: str = "groq",
        max_sliding_window_turns: int = 6,
        log_file: str = "chat_audit_log.jsonl",
    ):
        load_dotenv()
        self.provider = provider.lower()
        self.max_sliding_window_turns = max_sliding_window_turns
        self.log_file = log_file
        self.session_id = f"sess_{int(time.time())}"

        # Pricing per 1M tokens for telemetry (Groq standard)
        self.cost_per_1m_in = 0.59 if self.provider == "groq" else 0.00
        self.cost_per_1m_out = 0.79 if self.provider == "groq" else 0.00

        # Cumulative Session Metrics
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost_usd = 0.0
        self.total_messages_count = 0

        # Model mapping
        if self.provider == "groq":
            groq_key = os.getenv("GROQ_API_KEY")
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1", api_key=groq_key
            )
            self.model = "qwen/qwen3.8-27b"
        else:
            self.client = OpenAI(
                base_url="http://localhost:11434/v1", api_key="ollama"
            )
            self.model = "llama3.2:1b"

        # Conversation History (State)
        self.full_history: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def _get_pruned_messages(self) -> List[Dict[str, str]]:
        """Sliding Window: Always preserves System Prompt (index 0) + last N messages."""
        system_msg = self.full_history[0]
        recent_msgs = self.full_history[1:][-self.max_sliding_window_turns :]
        return [system_msg] + recent_msgs

    def _log_turn_to_audit_file(
        self,
        user_query: str,
        assistant_reply: str,
        in_tokens: int,
        out_tokens: int,
        turn_cost: float,
        latency_ms: float,
    ):
        """Appends a structured JSON log entry for auditing and fine-tuning."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "provider": self.provider,
            "model": self.model,
            "user_query": user_query,
            "assistant_reply": assistant_reply,
            "input_tokens": in_tokens,
            "output_tokens": out_tokens,
            "cost_usd": round(turn_cost, 6),
            "latency_ms": round(latency_ms, 1),
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def chat_turn(self, user_query: str):
        """Processes a single conversational turn with streaming, telemetry, and logging."""
        # 1. Append user message to full history
        self.full_history.append({"role": "user", "content": user_query})
        self.total_messages_count += 1

        # 2. Apply Sliding Window
        pruned_messages = self._get_pruned_messages()

        # Estimate input tokens (rough standard: ~1.3 tokens per word)
        in_tokens = int(
            sum(len(m["content"].split()) * 1.3 for m in pruned_messages)
        )

        print("👩‍💼 Ayesha: ", end="", flush=True)

        start_time = time.time()
        full_reply = ""
        out_token_count = 0

        # 3. Stream API Call
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=pruned_messages,
            temperature=0.3,
            max_tokens=200,
            stream=True,
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            if token:
                out_token_count += 1
                full_reply += token
                print(token, end="", flush=True)

        latency_ms = (time.time() - start_time) * 1000

        # 4. Append assistant response to history
        self.full_history.append(
            {"role": "assistant", "content": full_reply.strip()}
        )

        # 5. Telemetry & Cost Calculation
        turn_cost = (in_tokens / 1_000_000 * self.cost_per_1m_in) + (
            out_token_count / 1_000_000 * self.cost_per_1m_out
        )

        self.total_input_tokens += in_tokens
        self.total_output_tokens += out_token_count
        self.total_cost_usd += turn_cost

        # Print turn telemetry badge
        print(f"\n📊 [Turn Tokens: ~{in_tokens+out_token_count} (In:{in_tokens}, Out:{out_token_count}) | Cost: ${turn_cost:.6f} | Latency: {latency_ms:.0f}ms]")

        # 6. Audit Logging
        self._log_turn_to_audit_file(
            user_query,
            full_reply,
            in_tokens,
            out_token_count,
            turn_cost,
            latency_ms,
        )

    def print_session_summary(self):
        """Prints cumulative session telemetry upon exit."""
        print("\n" + "=" * 75)
        print("📈 CUMULATIVE CHAT SESSION SUMMARY")
        print("=" * 75)
        print(f"🆔 Session ID:              {self.session_id}")
        print(f"⚡ Active Provider:         {self.provider.upper()} ({self.model})")
        print(f"💬 Total Questions Handled: {self.total_messages_count}")
        print(f"📥 Total Input Tokens:      ~{self.total_input_tokens:,}")
        print(f"📤 Total Output Tokens:     ~{self.total_output_tokens:,}")
        print(f"💵 Total Session Cost:      ${self.total_cost_usd:.6f} USD")
        print(f"📝 Audit Log Saved:         {os.path.abspath(self.log_file)}")
        print("=" * 75)
        print("👋 Session ended gracefully. Khuda Hafiz!")


def main():
    print("=" * 75)
    print("🤖 PAKSTYLE APPAREL — PROFESSIONAL AI BUSINESS CHATBOT")
    print("=" * 75)
    print("Choose AI Inference Provider:")
    print("  1. Groq Cloud (Recommended: Ultra-Fast Qwen 27B)")
    print("  2. Local Ollama (100% Offline: Llama 3.2 1B)")

    choice = input("\nEnter choice (1 or 2, default is 1): ").strip()
    provider = "ollama" if choice == "2" else "groq"

    bot = ProductionBusinessChatbot(provider=provider)

    print(
        f"\n✅ Assistant Initialized using [{provider.upper()}]. Type 'exit' to quit."
    )
    print("-" * 75)

    while True:
        try:
            user_input = input("\n👤 Customer: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                bot.print_session_summary()
                break

            bot.chat_turn(user_input)

        except KeyboardInterrupt:
            bot.print_session_summary()
            break
        except Exception as e:
            print(f"\n❌ Error during turn: {e}")


if __name__ == "__main__":
    main()