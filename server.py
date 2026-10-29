from typing import Any
from fastmcp import FastMCP

mcp = FastMCP("Customer Operation")

CUSTOMERS = {
    "CUST-001": {"name": "Anu", "plan": "pro", "status": "active"},
    "CUST-002": {"name": "Rahul", "plan": "free", "status": "inactive"},
}

@mcp.tool
def get_customer(customer_id: str) -> dict[str, Any]:
    """Get safe customer account details using a customer ID.

    Args:
        customer_id: Customer identifier, for example CUST-001.
    """
    normalized_id = customer_id.upper()
    customer = CUSTOMERS.get(normalized_id)

    if customer is None:
        return {
            "found": False,
            "message": "Customer not found",
        }

    return {
        "found": True,
        "customer_id": normalized_id,
        **customer,
    }
@mcp.tool
def get_all_customers() -> dict[str, Any]:
    """Get all customer account details."""
    return {
        "customers": CUSTOMERS
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)