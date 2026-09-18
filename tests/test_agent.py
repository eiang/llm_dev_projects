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
