from typing import Any, Literal

from pydantic import BaseModel


class ToolResult(BaseModel):
    tool_name: str
    success: bool
    data: Any | None = None
    error_code: Literal["tool_not_found","invalid_tool_arguments","tool_execution_error"] | None = None
    error_message: str | None = None