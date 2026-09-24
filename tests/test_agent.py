from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from app.agents.order_agent import run_order_agent

def test_run_order_agent_direct_answer():
    messages = [
        {"role": "user", "content": "你好"}
    ]
    fake_message = MagicMock()
    fake_message.content = "你好,我是AI"
    fake_message.tool_calls = None
    fake_message.model_dump.return_value = {"role": "assistant", "content": "你好,我是AI"}
    with patch(
        "app.agents.order_agent.llm_client.complete",
        return_value=fake_message,
    ) as  mock_complete:
        result = run_order_agent(messages)  # pyright: ignore[reportArgumentType]
    assert result == "你好,我是AI"
    mock_complete.assert_called_once()

def test_run_order_agent_with_tool_call():
    messages = [
        {
            "role": "user",
            "content": "帮我查一下订单1001的状态",
        }
    ]
    tool_call = SimpleNamespace(
        id="call_001",
        function=SimpleNamespace(
            name="get_order_status",
            arguments='{"order_id": 1001}',
        )
    )
    first_message = MagicMock()
    first_message.content = None
    first_message.tool_calls = [tool_call]
    first_message.model_dump.return_value = {
        "role": "assistant",
        "tool_calls": [
            {
                "id": "call_001",
                "type": "function",
                "function": {
                    "name": "get_order_status",
                    "arguments": '{"order_id": 1001}',
                },
            }
        ],
    }

    second_message = MagicMock()
    second_message.content = "订单 1001 的 MacBook Pro 已经发货。"
    second_message.tool_calls = None
    second_message.model_dump.return_value = {
        "role": "assistant",
        "content": "订单 1001 的 MacBook Pro 已经发货。",
    }

    with patch(
        "app.agents.order_agent.llm_client.complete",
        side_effect=[
            first_message,
            second_message,
        ],
    ) as mock_complete:
        result = run_order_agent(messages)  # pyright: ignore[reportArgumentType]

    assert result == "订单 1001 的 MacBook Pro 已经发货。"
    assert mock_complete.call_count == 2
    assert len(messages) == 4
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
    assert messages[2]["role"] == "tool"
    assert messages[3]["role"] == "assistant"
    assert messages[2]["tool_call_id"] == "call_001"
    print(messages)