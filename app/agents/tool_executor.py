import json
import logging
import time
from inspect import signature

from app.schemas.tool import ToolResult

logger = logging.getLogger(__name__)

def execute_tool_call(
    tool_call,
    available_tools,
    trace_id: str,
    step: int,
) -> ToolResult:
    function_name = tool_call.function.name
    function = available_tools.get(function_name)
    if function is None:
        return ToolResult(
            tool_name=function_name,
            success=False,
            error_code="tool_not_found",
            error_message="Tool not found",
         )
    
    try:
        arguments= json.loads(tool_call.function.arguments)
    except json.JSONDecodeError:
        return ToolResult(
            tool_name=function_name,
            success=False,
            error_code="invalid_tool_arguments",
            error_message="Tool arguments are not valid JSON",
        )      
    try:
        signature(function).bind(**arguments)
    except TypeError:
        return ToolResult(
            tool_name=function_name,
            success=False,
            error_code="invalid_tool_arguments",
            error_message="Tool arguments are not valid",
        )
    start_time = time.perf_counter()
    try:
        result = function(**arguments)
    except Exception:
        duration_ms = (
            time.perf_counter() - start_time
            ) * 1000

        logger.exception(
                "event=tool_execution_failed trace_id=%s step=%d tool=%s duration_ms=%.2f",
                trace_id,
                step,
                function_name,
                duration_ms,
            )
        return ToolResult(
            tool_name=function_name,
            success=False,
            error_code="tool_execution_error",
            error_message="Tool execution error",
        )
    duration_ms = (
        time.perf_counter() - start_time
    ) * 1000

    logger.info(
        "event=tool_execution_completed trace_id=%s step=%d tool=%s duration_ms=%.2f",
        trace_id,
        step,
        function_name,
        duration_ms,
    )
    return ToolResult(
        tool_name=function_name,
        success=True,
        data=result,
    )
