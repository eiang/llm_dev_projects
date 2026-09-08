import json
from inspect import signature
from app.schemas.tool import ToolResult


def execute_tool_call(
    tool_call,
    available_tools,
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
    try:
        result = function(**arguments)
    except Exception:
        return ToolResult(
            tool_name=function_name,
            success=False,
            error_code="tool_execution_error",
            error_message="Tool execution error",
        )
    return ToolResult(
        tool_name=function_name,
        success=True,
        data=result,
    )
