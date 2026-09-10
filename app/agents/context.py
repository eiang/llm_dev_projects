from dataclasses import dataclass, field
import time

@dataclass
class AgentRunContext:
    trace_id: str
    step: int = 0
    llm_call_count: int = 0
    tool_call_count: int = 0
    start_time: float = field(default_factory=time.perf_counter)