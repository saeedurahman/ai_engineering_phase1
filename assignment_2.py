import os
import time
from dotenv import load_dotenv
from groq import Groq


def get_groq_client() -> Groq:
    """Loads environment and initializes the Groq client securely."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY nahi mili! Check karein ke .env file mojood hai."
        )

    return Groq(api_key=api_key)


def test_temperature_impact(
    client: Groq, prompt: str, temp: float, runs: int = 2
):
    """Runs the same prompt multiple times to observe determinism."""
    model_name = "qwen/qwen3.8-27b"

    print("\n" + "=" * 70)
    print(f"🧪 TESTING WITH TEMPERATURE: {temp}")
    print("=" * 70)

    for i in range(1, runs + 1):
        start_time = time.time()

        # Groq API Call
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=temp,
            max_tokens=60,  # Token limit taake response mukhtasir rahe
        )

        elapsed_time = (time.time() - start_time) * 1000  # in ms
        content = response.choices[0].message.content.strip()
        usage = response.usage

        print(f"\n[Run #{i}] (Latency: {elapsed_time:.1f}ms)")
        print(f"👉 AI Response: \"{content}\"")
        print(
            f"📊 Tokens: Input={usage.prompt_tokens} | Output={usage.completion_tokens} | Total={usage.total_tokens}"
        )


if __name__ == "__main__":
    client = get_groq_client()

    # Creative / Open-ended prompt jo temperature ka farq saaf dikhaye
    test_prompt = "Ek line mein batayein ke Artificial Intelligence kya hai?"

    print("🚀 GROQ API PARAMETER & TOKEN METRICS EXPERIMENT")

    # Experiment 1: Temperature 0.0 (Har dafa exact same aana chahiye)
    test_temperature_impact(client, test_prompt, temp=0.0, runs=2)

    # Experiment 2: Temperature 1.2 (Har dafa lafz aur style badalna chahiye)
    test_temperature_impact(client, test_prompt, temp=1.2, runs=2)