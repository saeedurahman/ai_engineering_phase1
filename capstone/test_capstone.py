import json
import pytest
from capstone.agent import BusinessAgent
from capstone.config import SUPPORTED_MODELS
from capstone.logger import SessionTelemetryLogger
from capstone.tools import execute_tool, track_order_status


# =====================================================================
# 1. CONFIGURATION INTEGRITY TEST
# =====================================================================
def test_config_models_integrity():
    """Verifies that all required providers and models are cataloged with pricing."""
    assert "groq-qwen" in SUPPORTED_MODELS
    assert "ollama-llama" in SUPPORTED_MODELS

    groq_model = SUPPORTED_MODELS["groq-qwen"]
    assert groq_model.provider == "groq"
    assert groq_model.input_cost_per_1m > 0
    assert groq_model.output_cost_per_1m > 0


# =====================================================================
# 2. TOOLS & DATABASE EXECUTION TEST
# =====================================================================
def test_tools_order_tracking_success():
    """Verifies real Python order tracking tool execution."""
    raw_result = execute_tool("track_order_status", {"order_id": "102"})
    data = json.loads(raw_result)

    assert data["success"] is True
    assert data["data"]["status"] == "IN_TRANSIT"
    assert data["data"]["courier"] == "TCS Express"
    assert "Hamza" in data["data"]["rider_name"]


def test_tools_order_tracking_not_found():
    """Verifies clean error handling for non-existent order ID."""
    raw_result = execute_tool("track_order_status", {"order_id": "99999"})
    data = json.loads(raw_result)

    assert data["success"] is False
    assert "nahi mila" in data["error"]


# =====================================================================
# 3. TELEMETRY & COST MATH TEST
# =====================================================================
def test_telemetry_cost_math():
    """Verifies that dollar cost math is accurate based on 1M rates."""
    logger = SessionTelemetryLogger(log_file="test_audit_temp.jsonl")
    groq_model = SUPPORTED_MODELS["groq-qwen"]

    # 1,000 in ($0.59/1M) + 500 out ($0.79/1M)
    cost = logger.compute_turn_cost(1000, 500, groq_model)
    expected = (1000 / 1_000_000 * 0.59) + (500 / 1_000_000 * 0.79)

    assert abs(cost - expected) < 1e-9


# =====================================================================
# 4. SLIDING WINDOW MEMORY PRUNING TEST
# =====================================================================
def test_sliding_window_preserves_system_prompt():
    """Verifies that sliding window never drops System Prompt and limits history."""
    agent = BusinessAgent(max_history=4)

    # 8 dummy messages add karte hain
    for i in range(8):
        agent.full_history.append({"role": "user", "content": f"Msg {i}"})

    pruned = agent._get_pruned_messages()

    # Total messages should be: 1 (System) + 4 (recent) = 5
    assert len(pruned) == 5
    assert pruned[0]["role"] == "system"
    assert pruned[-1]["content"] == "Msg 7"


# =====================================================================
# 5. END-TO-END AUTONOMOUS AGENT TEST
# =====================================================================
def test_end_to_end_agent_response():
    """Verifies end-to-end agent completion and factual accuracy."""
    agent = BusinessAgent(model_key="groq-qwen")

    # Direct query test
    agent.handle_user_query(
        "Assalam o Alaikum, Karachi ke liye delivery charges kitne hain?"
    )
    last_reply = agent.full_history[-1]["content"]

    assert "200" in last_reply