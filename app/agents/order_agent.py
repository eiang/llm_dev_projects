import logging
import time
import uuid

from app.agents.context import AgentRunContext
from app.agents.tool_executor import execute_tool_call
from app.clients import llm_client
from app.schemas.tool import ToolResult
from app.tools.order_tools import AVAILABLE_TOOLS, TOOLS


def _append_tool_message(messages: list[dict[str,object]], 
tool_call_id: str, result: ToolResult) -> None:
    tool_message: dict[str,object] = {
        "role": "tool",
        "content": result.model_dump_json(exclude_none=True),
        "tool_call_id": tool_call_id,
    }
    
    messages.append(tool_message)  

logger = logging.getLogger(__name__)

def run_order_agent(messages: list[dict[str,object]],max_steps: int = 5) -> str:
    trace_id = uuid.uuid4().hex
    context = AgentRunContext(trace_id=trace_id)
    logger.info(
        "event=agent_started trace_id=%s",
        context.trace_id,
    )
    try:
        for step in range(max_steps):
            context.step = step + 1
            logger.info(
                "event=agent_step_started trace_id=%s step=%s max_steps=%s",
                context.trace_id,
                context.step,
                max_steps,
            )
            
            context.llm_call_count += 1
            message = llm_client.complete(messages,tools=TOOLS)
            logger.info(
                "event=llm_call_completed trace_id=%s step=%s llm_call_count=%s",
                context.trace_id,
                context.step,
                context.llm_call_count,
            )
            messages.append(message.model_dump(exclude_none=True,exclude={"reasoning_content"}))
            logger.debug(
                "event=messages_updated trace_id=%s message_count=%s",
                context.trace_id,
                len(messages),
            )
            
            if not message.tool_calls:
                if message.content is None:
                    raise llm_client.LlmError(
                        "LLM returned no content"
                    )
              
                logger.info(
                    "event=agent_completed trace_id=%s step=%s ",
                    context.trace_id,
                    context.step,
                    
                )
               
                return message.content
            
            for tool_call in message.tool_calls:
                context.tool_call_count += 1
                logger.info(
                    "event=tool_call_started trace_id=%s step=%s tool=%s tool_call_count=%s",
                    context.trace_id,
                    context.step,
                    tool_call.function.name,
                    context.tool_call_count,
                )
                tool_result  = execute_tool_call(
                    tool_call,
                    available_tools=AVAILABLE_TOOLS,
                    trace_id=context.trace_id,
                    step=context.step,
                )
                if tool_result.success:
                    logger.info(
                        "event=tool_call_completed trace_id=%s step=%s tool=%s tool_call_count=%s",
                        context.trace_id,
                        context.step,
                        tool_result.tool_name,
                        context.tool_call_count,
                    )
                else:
                    logger.error(
                        "event=tool_call_failed trace_id=%s step=%s tool=%s error_code=%s",
                        context.trace_id,
                        context.step,
                        tool_result.tool_name,
                        tool_result.error_code,
                    )
                _append_tool_message(messages, tool_call.id, tool_result )
    finally: 
        duration_ms = (time.perf_counter() - context.start_time) * 1000
        logger.info(
            "event=agent_finished trace_id=%s llm_call_count=%s tool_call_count=%s duration=%.2f",
            context.trace_id,
            context.llm_call_count,
            context.tool_call_count,
            duration_ms,
        )
    raise RuntimeError(f"Agent exceed max_steps: {max_steps}")




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    messages: list[dict[str,object]] = [
        {
            "role": "user",
            "content": "帮我查一下订单 1001 的状态，并用自然语言告诉我。",
        }
    ]
    answer = run_order_agent(messages)  

    print("final answer:", answer)
    print("final messages:", messages)
        

    