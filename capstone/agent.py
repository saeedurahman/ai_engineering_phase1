import json
import time
from typing import Dict, List, Optional
from capstone.client import MultiProviderAIClient
from capstone.config import (
    BUSINESS_SYSTEM_PROMPT,
    DEFAULT_MODEL_KEY,
    MAX_SLIDING_WINDOW_MESSAGES,
)
from capstone.logger import SessionTelemetryLogger
from capstone.tools import TOOLS_REGISTRY, execute_tool


class BusinessAgent:
    """Production Autonomous Agent orchestrating sliding window memory, tool execution, and telemetry."""

    def __init__(
        self,
        model_key: str = DEFAULT_MODEL_KEY,
        max_history: int = MAX_SLIDING_WINDOW_MESSAGES,
    ):
        self.client = MultiProviderAIClient(initial_model_key=model_key)
        self.logger = SessionTelemetryLogger()
        self.max_history = max_history

        # Conversation History (State)
        self.full_history: List[Dict[str, str]] = [
            {"role": "system", "content": BUSINESS_SYSTEM_PROMPT}
        ]

    def _get_pruned_messages(self) -> List[Dict[str, str]]:
        """Sliding Window: Preserves System Prompt (index 0) + last N messages."""
        system_msg = self.full_history[0]
        recent_msgs = self.full_history[1:][-self.max_history :]
        return [system_msg] + recent_msgs

    def handle_user_query(self, user_query: str):
        """Executes a full turn with tool detection, execution, streaming, and telemetry."""
        # 1. User message state mein add karein
        self.full_history.append({"role": "user", "content": user_query})
        pruned_messages = self._get_pruned_messages()

        start_time = time.time()
        in_tokens = int(
            sum(len(m["content"].split()) * 1.3 for m in pruned_messages)
        )
        tool_executed_name: Optional[str] = None
        full_reply = ""
        out_token_count = 0

        # 2. First API Call: Send Query + Tools to determine intent
        # Agar Groq model ho toh tools enable karein
        tools_to_pass = (
            TOOLS_REGISTRY if self.client.active_model_info.provider == "groq" else None
        )

        first_response = self.client.create_completion(
            messages=pruned_messages,
            tools=tools_to_pass,
            stream=False,  # Tool detection synchronous hoti hai
            temperature=0.0,
            max_tokens=150,
        )

        response_message = first_response.choices[0].message
        tool_calls = getattr(response_message, "tool_calls", None)

        # 3. Decision Branching: Tool Call ya Direct Chat?
        if tool_calls:
            # --- TOOL EXECUTION WORKFLOW ---
            tool_call = tool_calls[0]
            function_name = tool_call.function.name
            tool_executed_name = function_name
            args = json.loads(tool_call.function.arguments)

            print(f"\n⚙️  [AUTONOMOUS TOOL TRIGGERED]: {function_name}({args})")

            # Run Python Tool
            tool_result = execute_tool(function_name, args)
            print(f"📡 [DATABASE RESULT]: {tool_result}\n")

            # Update conversation history with tool interaction
            self.full_history.append(response_message)
            self.full_history.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": tool_result,
                }
            )

            # Second API Call: Stream final polite explanation
            print("👩‍💼 Ayesha: ", end="", flush=True)
            stream_response = self.client.create_completion(
                messages=self._get_pruned_messages(),
                stream=True,
                temperature=0.3,
                max_tokens=200,
            )

            for chunk in stream_response:
                token = chunk.choices[0].delta.content or ""
                if token:
                    out_token_count += 1
                    full_reply += token
                    print(token, end="", flush=True)

        else:
            # --- DIRECT CHAT WORKFLOW ---
            direct_content = response_message.content or ""
            print("👩‍💼 Ayesha: ", end="", flush=True)

            # Print direct response
            for word in direct_content.split(" "):
                print(word + " ", end="", flush=True)
                time.sleep(0.01)  # Smooth typewriter simulation

            full_reply = direct_content
            out_token_count = len(direct_content.split())

        latency_ms = (time.time() - start_time) * 1000

        # 4. Final response memory mein add karein
        self.full_history.append(
            {"role": "assistant", "content": full_reply.strip()}
        )

        # 5. Record Telemetry & Audit Log
        entry = self.logger.record_turn(
            user_query=user_query,
            assistant_reply=full_reply,
            in_tokens=in_tokens,
            out_tokens=out_token_count,
            model_info=self.client.active_model_info,
            latency_ms=latency_ms,
            tool_executed=tool_executed_name,
        )

        # Print Telemetry Badge
        print(
            f"\n📊 [Turn Cost: ${entry['cost_usd']:.6f} | Tokens: In={in_tokens}, Out={out_token_count} | Latency: {latency_ms:.0f}ms]"
        )