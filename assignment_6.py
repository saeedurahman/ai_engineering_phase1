import time
from openai import OpenAI


def get_local_ollama_client() -> OpenAI:
    """Initializes an OpenAI-compatible client pointing to LOCAL Ollama on port 11434.

    Notice: No real API key or internet required!
    """
    return OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # Local Ollama ko kisi key ki zaroorat nahi hoti
    )


def test_local_model_inference():
    client = get_local_ollama_client()
    model_name = "llama3.2:1b"

    prompt = "Ek chhota paragraph Roman Urdu mein likhein ke offline AI software apps ke liye kyun zaroori hai?"

    print("=" * 75)
    print("🏠 LOCAL AI INFERENCE TEST (100% OFFLINE ON YOUR OWN HARDWARE)")
    print(f"🤖 Model: {model_name} | Host: http://localhost:11434")
    print("=" * 75)
    print(f"👤 Prompt: \"{prompt}\"")
    print("\n🤖 Local Llama (Streaming Response): ", end="", flush=True)

    start_time = time.time()
    first_token_time = None
    token_count = 0

    try:
        # OpenAI-compatible streaming call to LOCAL OLLAMA
        stream = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Answer in clear Roman Urdu.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=200,
            stream=True,
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            if token:
                if first_token_time is None:
                    first_token_time = (time.time() - start_time) * 1000
                token_count += 1
                print(token, end="", flush=True)

        total_time = time.time() - start_time

        print("\n\n" + "-" * 75)
        print("📊 LOCAL HARDWARE PERFORMANCE BENCHMARK:")
        print(f"⏱️  Time To First Token (TTFT): {first_token_time:.0f}ms")
        print(f"⏳ Total Generation Time: {total_time:.2f} seconds")
        if total_time > 0:
            speed = token_count / total_time
            print(f"⚡ Local Inference Speed: {speed:.1f} tokens/second")
        print("🔐 Privacy Status: 100% OFFLINE (Zero Data Sent to Cloud)")
        print("-" * 75)

    except Exception as e:
        print(f"\n❌ Error connecting to Ollama: {e}")
        print(
            "💡 Hint: Check karein ke Ollama background mein chal raha hai ya nahi."
        )


if __name__ == "__main__":
    test_local_model_inference()