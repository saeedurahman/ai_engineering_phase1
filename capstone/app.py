import sys
from capstone.agent import BusinessAgent
from capstone.config import SUPPORTED_MODELS


def display_banner():
    print("=" * 80)
    print("🌟 PAKSTYLE APPAREL — MULTI-PROVIDER AUTONOMOUS AI BUSINESS ASSISTANT")
    print("=" * 80)
    print("Supported AI Inference Engines:")
    print("  1. groq-qwen    -> Qwen 27B on Groq Cloud (Recommended: Blazing Fast + Tools)")
    print("  2. ollama-llama -> Llama 3.2 1B (Local: 100% Offline & Private)")
    print("  3. ollama-qwen  -> Qwen 2.5 0.5B (Local: Ultra-Lightweight)")
    print("=" * 80)
    print("Special Commands: '/switch' (change model), '/stats' (view costs), 'exit' (quit)")
    print("-" * 80)


def choose_initial_model() -> str:
    choice = input("\nSelect Engine [1, 2, or 3] (Default: 1): ").strip()
    mapping = {
        "1": "groq-qwen",
        "2": "ollama-llama",
        "3": "ollama-qwen",
        "groq": "groq-qwen",
        "ollama": "ollama-llama",
    }
    return mapping.get(choice, "groq-qwen")


def main():
    display_banner()
    initial_key = choose_initial_model()

    agent = BusinessAgent(model_key=initial_key)
    print(f"\n✅ Assistant Initialized with [{agent.client.active_model_info.name}]. Ready to chat!")
    print("-" * 80)

    while True:
        try:
            user_input = input("\n👤 Customer: ").strip()

            if not user_input:
                continue

            # Command Handling
            if user_input.lower() in ["exit", "quit", "q"]:
                summary = agent.logger.get_summary()
                print("\n" + "=" * 80)
                print("📈 CUMULATIVE SESSION AUDIT SUMMARY")
                print("=" * 80)
                print(f"🆔 Session ID:              {summary['session_id']}")
                print(f"💬 Total Questions Handled: {summary['total_turns']}")
                print(f"📥 Total Input Tokens:      ~{summary['total_input_tokens']:,}")
                print(f"📤 Total Output Tokens:     ~{summary['total_output_tokens']:,}")
                print(f"⚡ Total Tokens Processed:  ~{summary['total_tokens']:,}")
                print(f"💵 Total API Bill:          ${summary['total_cost_usd']:.6f} USD")
                print(f"📝 Audit Trail File:        {summary['log_file_path']}")
                print("=" * 80)
                print("👋 Khuda Hafiz! Session ended.")
                break

            elif user_input.lower() == "/stats":
                s = agent.logger.get_summary()
                print(f"\n📊 [SESSION STATS]: Turns: {s['total_turns']} | Tokens: ~{s['total_tokens']:,} | Cost: ${s['total_cost_usd']:.6f}")
                continue

            elif user_input.lower() == "/switch":
                print("\nAvailable Models to Switch:")
                for k, v in SUPPORTED_MODELS.items():
                    print(f"  - {k:<15} ({v.name})")
                new_key = input("Enter model key: ").strip().lower()
                if new_key in SUPPORTED_MODELS:
                    agent.client.switch_model(new_key)
                else:
                    print("❌ Invalid model key!")
                continue

            # Hand over to Autonomous Agent
            agent.handle_user_query(user_input)

        except KeyboardInterrupt:
            print("\n👋 Process terminated by user.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()