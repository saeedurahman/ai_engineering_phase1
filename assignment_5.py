import os
import time
from typing import Dict, List
from dotenv import load_dotenv
import groq
from groq import Groq


def get_groq_client() -> Groq:
    """Loads environment and initializes Groq client."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY nahi mili! .env file check karein.")
    return Groq(api_key=api_key)


SYSTEM_PROMPT = """
You are an intelligent, polite AI Assistant. 
You communicate fluently in English and Roman Urdu.
Keep your answers concise, helpful, and direct.
"""


def call_groq_with_retry(
    client: Groq,
    messages: List[Dict[str, str]],
    model_name: str = "qwen/qwen3.8-27b",
    max_retries: int = 3,
):
    """Executes a streaming Groq API call protected with Exponential Backoff."""
    for attempt in range(max_retries):
        try:
            stream = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.3,
                max_tokens=250,
                stream=True,  # 👈 Real-time streaming
            )
            return stream

        except groq.RateLimitError as e:
            wait_time = 2**attempt  # Exponential backoff: 1s, 2s, 4s
            print(
                f"\n⚠️ [RATE LIMIT HIT (429)]: Groq busy hai. {wait_time}s mein retry kar rahe hain (Attempt {attempt+1}/{max_retries})..."
            )
            time.sleep(wait_time)

        except groq.APIConnectionError:
            print(
                f"\n⚠️ [CONNECTION ERROR]: Network issue. 2s mein retry kar rahe hain..."
            )
            time.sleep(2)

    raise RuntimeError("❌ Max retries exceed ho gaye. API call fail ho gayi.")


def run_interactive_streaming_bot():
    """Runs interactive multi-turn streaming chatbot in terminal."""
    client = get_groq_client()
    model_name = "qwen/qwen3.8-27b"

    print("=" * 75)
    print("🤖 GROQ STREAMING AI CHATBOT (Type 'exit' to quit)")
    print(f"⚡ Model: {model_name} | Real-Time Typewriter Streaming ON")
    print("=" * 75)

    # Conversation Memory
    conversation_history: List[Dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "q"]:
                print("\n👋 Khuda Hafiz! Chat session ended.")
                break

            # 1. User message history mein add karein
            conversation_history.append(
                {"role": "user", "content": user_input}
            )

            print("🤖 AI: ", end="", flush=True)

            start_time = time.time()
            first_token_received = False
            ttft = 0.0

            # 2. Resilient Streaming Call
            stream = call_groq_with_retry(
                client, conversation_history, model_name=model_name
            )

            full_assistant_reply = ""

            for chunk in stream:
                token_text = chunk.choices[0].delta.content or ""

                # Time To First Token (TTFT) measurement
                if token_text and not first_token_received:
                    ttft = (time.time() - start_time) * 1000
                    first_token_received = True

                full_assistant_reply += token_text
                # Live typing effect
                print(token_text, end="", flush=True)

            total_latency = (time.time() - start_time) * 1000

            # 3. Assistant response memory mein add karein taake pichli baat yaad rahe
            conversation_history.append(
                {"role": "assistant", "content": full_assistant_reply}
            )

            print(
                f"\n⏱️  [Latency: {total_latency:.0f}ms | TTFT: {ttft:.0f}ms]"
            )

        except KeyboardInterrupt:
            print("\n👋 Process stopped by user.")
            break


if __name__ == "__main__":
    run_interactive_streaming_bot()