import os
import time
from typing import Dict, Generator, List, Optional
from dotenv import load_dotenv
from openai import OpenAI


class UnifiedAIClient:
    """Production-grade Provider-Agnostic Client supporting Groq, Ollama, and Auto-Failover."""

    def __init__(
        self,
        default_provider: str = "groq",
        groq_model: str = "qwen/qwen3.8-27b",
        ollama_model: str = "llama3.2:1b",
    ):
        load_dotenv()
        self.default_provider = default_provider.lower()
        self.groq_model = groq_model
        self.ollama_model = ollama_model

        # 1. Groq Client (OpenAI-compatible client pointing to Groq)
        groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=groq_api_key or "missing_key",
        )

        # 2. Local Ollama Client (OpenAI-compatible client pointing to localhost:11434)
        self.ollama_client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )

    def generate(
        self,
        messages: List[Dict[str, str]],
        provider: Optional[str] = None,
        stream: bool = True,
        enable_failover: bool = True,
    ) -> Generator[str, None, None]:
        """Unified method to stream AI responses from any provider with automatic failover."""
        chosen_provider = (provider or self.default_provider).lower()

        try:
            # Route to chosen provider
            if chosen_provider == "groq":
                client = self.groq_client
                model = self.groq_model
            elif chosen_provider == "ollama":
                client = self.ollama_client
                model = self.ollama_model
            else:
                raise ValueError(
                    f"Unknown AI provider: {chosen_provider}. Use 'groq' or 'ollama'."
                )

            # Unified API Call (OpenAI Standard)
            response_stream = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,
                max_tokens=200,
                stream=stream,
            )

            for chunk in response_stream:
                token = chunk.choices[0].delta.content or ""
                if token:
                    yield token

        except Exception as primary_error:
            # 🛡️ AUTOMATIC FAILOVER LOGIC
            if enable_failover and chosen_provider == "groq":
                print(
                    f"\n⚠️  [FAILOVER TRIGGERED]: Cloud Groq failed ({primary_error.__class__.__name__})!"
                )
                print(
                    f"🔄 Switching automatically to LOCAL OLLAMA ({self.ollama_model})...\n"
                )

                # Fallback to Local Ollama
                fallback_stream = self.ollama_client.chat.completions.create(
                    model=self.ollama_model,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=200,
                    stream=stream,
                )

                for chunk in fallback_stream:
                    token = chunk.choices[0].delta.content or ""
                    if token:
                        yield token
            else:
                raise primary_error


# =====================================================================
# 🧪 APPLICATION BUSINESS LOGIC (Zero Provider Knowledge!)
# =====================================================================
def run_business_conversation(
    client: UnifiedAIClient, query: str, provider: Optional[str] = None
):
    """Notice: This business function does NOT care which provider is running!"""
    messages = [
        {
            "role": "system",
            "content": "You are a helpful customer support agent. Answer concisely in Roman Urdu.",
        },
        {"role": "user", "content": query},
    ]

    print(
        f"\n[REQUEST] User: '{query}' | Target Provider: {provider or client.default_provider.upper()}"
    )
    print("🤖 AI Response: ", end="", flush=True)

    start_time = time.time()
    for token in client.generate(messages, provider=provider):
        print(token, end="", flush=True)

    elapsed = time.time() - start_time
    print(f"\n⏱️  Completed in {elapsed:.2f}s")


if __name__ == "__main__":
    ai_client = UnifiedAIClient(default_provider="groq")

    print("=" * 80)
    print("🚀 UNIFIED PROVIDER-AGNOSTIC CLIENT ARCHITECTURE TEST")
    print("=" * 80)

    # Test 1: Cloud Groq Call
    print("\n--- TEST 1: Explicit Groq Cloud Request ---")
    run_business_conversation(
        ai_client,
        "Assalam o Alaikum, 1 line mein batayein Cloud AI ka kya faida hai?",
        provider="groq",
    )

    # Test 2: Local Ollama Call
    print("\n--- TEST 2: Explicit Local Ollama Request ---")
    run_business_conversation(
        ai_client,
        "Assalam o Alaikum, 1 line mein batayein Local AI ka kya faida hai?",
        provider="ollama",
    )

    # Test 3: Simulation of Automatic Failover
    print("\n--- TEST 3: Cloud Failure Simulation (Auto-Failover to Ollama) ---")
    # Jaan boojh kar Cloud key kharab karte hain taake failover trigger ho
    ai_client.groq_client.api_key = "invalid_broken_key"
    run_business_conversation(
        ai_client,
        "Mera order kab milega?",
        provider="groq",  # Mangenge Groq, lekin failover Ollama par hoga!
    )