import os
import time
from typing import Any, Dict, List, Optional
from openai import OpenAI
from capstone.config import DEFAULT_MODEL_KEY, SUPPORTED_MODELS, ModelInfo


class MultiProviderAIClient:
    """Unified client handling Groq, Ollama, model switching, and resilient auto-failover."""

    def __init__(self, initial_model_key: str = DEFAULT_MODEL_KEY):
        self.active_model_key = initial_model_key
        self.active_model_info: ModelInfo = SUPPORTED_MODELS[initial_model_key]

        # 1. Groq Cloud Client
        groq_key = os.getenv("GROQ_API_KEY")
        self.groq_client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=groq_key or "missing_key",
        )

        # 2. Local Ollama Client
        self.ollama_client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )

    def switch_model(self, model_key: str):
        """Allows runtime switching between supported cloud and local models."""
        if model_key not in SUPPORTED_MODELS:
            raise ValueError(
                f"Unknown model key: {model_key}. Available: {list(SUPPORTED_MODELS.keys())}"
            )
        self.active_model_key = model_key
        self.active_model_info = SUPPORTED_MODELS[model_key]
        print(f"\n🔄 [MODEL SWITCHED]: Now using {self.active_model_info.name}")

    def get_active_client(self) -> OpenAI:
        """Returns the appropriate OpenAI client instance for the active model."""
        if self.active_model_info.provider == "groq":
            return self.groq_client
        else:
            return self.ollama_client

    def create_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
        temperature: float = 0.3,
        max_tokens: int = 250,
        enable_failover: bool = True,
    ):
        """Unified completion call with automatic Cloud -> Local Failover protection."""
        client = self.get_active_client()
        model_id = self.active_model_info.id

        params: Dict[str, Any] = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        if tools:
            params["tools"] = tools
            params["tool_choice"] = "auto"

        try:
            return client.chat.completions.create(**params)

        except Exception as primary_error:
            # 🛡️ AUTOMATIC FAILOVER PROTECTION
            if (
                enable_failover
                and self.active_model_info.provider == "groq"
            ):
                print(
                    f"\n⚠️  [FAILOVER ALERT]: Cloud ({self.active_model_info.name}) failed!"
                )
                print(
                    "🔄 Seamlessly falling back to LOCAL OLLAMA (llama3.2:1b)...\n"
                )

                # Fallback to local Ollama
                fallback_params = params.copy()
                fallback_params["model"] = "llama3.2:1b"
                return self.ollama_client.chat.completions.create(
                    **fallback_params
                )
            else:
                raise primary_error