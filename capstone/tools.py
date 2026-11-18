import json
from typing import Any, Dict, List

# =====================================================================
# 📦 MOCK COURIER & ORDERS DATABASE
# =====================================================================
ORDERS_DB: Dict[str, Dict[str, Any]] = {
    "101": {
        "order_id": "101",
        "customer": "Ali Raza",
        "city": "Karachi",
        "items": "Silk Kurta (Navy Blue, Size L)",
        "courier": "TCS Express",
        "tracking_num": "TCS-987654",
        "status": "DELIVERED",
        "delivery_date": "16 Nov 2026",
    },
    "102": {
        "order_id": "102",
        "customer": "Sara Ahmed",
        "city": "Lahore",
        "items": "Lawn 3-Piece Stitched Suit",
        "courier": "TCS Express",
        "tracking_num": "TCS-112233",
        "status": "IN_TRANSIT",
        "rider_name": "Hamza",
        "expected_delivery": "Today by 5:00 PM",
    },
    "103": {
        "order_id": "103",
        "customer": "Usman Tariq",
        "city": "Islamabad",
        "items": "Pure Leather Formal Jacket",
        "courier": "Leopards Courier",
        "tracking_num": "LEO-554433",
        "status": "PROCESSING",
        "expected_delivery": "2-3 working days",
    },
}


# =====================================================================
# ⚙️ REAL PYTHON EXECUTION FUNCTIONS
# =====================================================================
def track_order_status(order_id: str) -> str:
    """Queries the database and returns structured shipping status."""
    clean_id = str(order_id).strip().replace("#", "").replace("PK-", "")

    if clean_id in ORDERS_DB:
        order = ORDERS_DB[clean_id]
        return json.dumps({"success": True, "data": order})
    else:
        return json.dumps(
            {
                "success": False,
                "error": f"Order #{clean_id} database mein nahi mila. Please Order ID re-check karein.",
            }
        )


# =====================================================================
# 🛠️ OPENAI-COMPATIBLE TOOL SCHEMAS
# =====================================================================
TOOLS_REGISTRY: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "track_order_status",
            "description": "Fetches real-time shipping, courier, rider details, and tracking status for a customer's order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The numeric order ID, e.g., '101', '102', '103'.",
                    }
                },
                "required": ["order_id"],
            },
        },
    }
]


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Dispatcher function that runs the appropriate Python tool dynamically."""
    if tool_name == "track_order_status":
        order_id = arguments.get("order_id", "")
        return track_order_status(order_id=order_id)
    else:
        return json.dumps({"success": False, "error": f"Unknown tool: {tool_name}"})