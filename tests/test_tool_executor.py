
from types import SimpleNamespace


from app.agents.tool_executor import execute_tool_call
from app.tools.order_tools import AVAILABLE_TOOLS





def test_execute_tool_call_success():
    tool_call = SimpleNamespace(
    function=SimpleNamespace(
        name="get_order_status",
        arguments='{"order_id": 1001}',
    )
    )
    result = execute_tool_call(
        tool_call,
        available_tools=AVAILABLE_TOOLS,
    )
    assert result.success 
    assert result.data == {
            "status": "shipped",
            "product": "MacBook Pro",
        }

def test_execute_tool_call_tool_not_found():
    tool_call1 = SimpleNamespace(
    function=SimpleNamespace(
        name="get_order_status_1",
        arguments='{"order_id": 1001}',
    )
)
    result = execute_tool_call(
        tool_call1,
        available_tools=AVAILABLE_TOOLS,
    )
    assert result.success == False
    assert result.error_code == "tool_not_found"
    assert result.error_message == "Tool not found"

def test_execute_tool_call_invalid_json():
    tool_call2 = SimpleNamespace(
    function=SimpleNamespace(
        name="get_order_status",
        arguments='{"order_id": 1001',
    )
)
    result = execute_tool_call(
        tool_call2,
        available_tools=AVAILABLE_TOOLS,
    )
    assert result.success == False
    assert result.error_code == "invalid_tool_arguments"
    assert result.error_message == "Tool arguments are not valid JSON"

def test_execute_tool_call_invalid_arguments():
    tool_call3 = SimpleNamespace(
    function=SimpleNamespace(
        name="get_order_status",
        arguments='{"order": 1001}',
    )
)
    result = execute_tool_call(
        tool_call3,
        available_tools=AVAILABLE_TOOLS,
    )
    assert result.success == False
    assert result.error_code == "invalid_tool_arguments"
    assert result.error_message == "Tool arguments are not valid"



def broken_tool(order_id: int):
    raise RuntimeError("boom")
def test_execute_tool_call_execution_error():
    tool_call = SimpleNamespace(
        function=SimpleNamespace(
            name="broken_tool",
            arguments='{"order_id": 1001}',
        )
    )

    available_tools = {
        "broken_tool": broken_tool,
    }

    result = execute_tool_call(
        tool_call,
        available_tools=available_tools,
    )

    assert result.success is False
    assert result.error_code == "tool_execution_error"
    assert result.error_message == "Tool execution error"
