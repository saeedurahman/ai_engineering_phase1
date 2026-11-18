from datetime import datetime
import json
import os
import time
from typing import Any, Dict, Optional
from capstone.config import AUDIT_LOG_FILE, ModelInfo


class SessionTelemetryLogger:
    """Tracks token usage, computes real-time dollar cost, and persists structured audit logs."""

    def __init__(self, log_file: str = AUDIT_LOG_FILE):
        self.log_file = log_file
        self.session_id = f"sess_{int(time.time())}"

        # Cumulative Metrics
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost_usd = 0.0
        self.total_turns_count = 0

    def compute_turn_cost(
        self, in_tokens: int, out_tokens: int, model_info: ModelInfo
    ) -> float:
        """Calculates exact dollar cost using official per 1M token rates."""
        in_cost = (in_tokens / 1_000_000) * model_info.input_cost_per_1m
        out_cost = (out_tokens / 1_000_000) * model_info.output_cost_per_1m
        return in_cost + out_cost

    def record_turn(
        self,
        user_query: str,
        assistant_reply: str,
        in_tokens: int,
        out_tokens: int,
        model_info: ModelInfo,
        latency_ms: float,
        tool_executed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Records telemetry metrics and appends entry to JSONL audit file."""
        turn_cost = self.compute_turn_cost(in_tokens, out_tokens, model_info)

        # Update cumulative session stats
        self.total_input_tokens += in_tokens
        self.total_output_tokens += out_tokens
        self.total_cost_usd += turn_cost
        self.total_turns_count += 1

        entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "provider": model_info.provider,
            "model_id": model_info.id,
            "user_query": user_query,
            "assistant_reply": assistant_reply,
            "tool_executed": tool_executed,
            "input_tokens": in_tokens,
            "output_tokens": out_tokens,
            "total_turn_tokens": in_tokens + out_tokens,
            "cost_usd": round(turn_cost, 6),
            "latency_ms": round(latency_ms, 1),
        }

        # Append to JSONL log file
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return entry

    def get_summary(self) -> Dict[str, Any]:
        """Returns comprehensive session metrics dictionary."""
        return {
            "session_id": self.session_id,
            "total_turns": self.total_turns_count,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost_usd": round(self.total_cost_usd, 6),
            "log_file_path": os.path.abspath(self.log_file),
        }