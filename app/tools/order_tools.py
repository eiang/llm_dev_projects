def get_order_status(order_id: int) -> dict[str,str]:
    orders = {
        1001: {
            "status": "shipped",
            "product": "MacBook Pro",
        },
        1002: {
            "status": "processing",
            "product": "iPhone",
        },
    }

    return orders.get(
        order_id,
        {
            "status": "not_found",
        },
    )


GET_ORDER_STATUS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_order_status",
        "description": "Get the status of an order by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "integer",
                    "description": "The ID of the order to get the status of the order",
                },
            },
            "required": ["order_id"],
        },
    },
}



TOOLS = [
    GET_ORDER_STATUS_TOOL,
]