from typing import NamedTuple


class SimulationParameters(NamedTuple):
    request_duration_ms: int
    requests_per_day: int
    max_wait: int = 1

    def __str__(self) -> str:
        return f"Simulation: [{self.requests_per_day}x" \
               f"{self.request_duration_ms}ms req/day, " \
               f"{self.max_wait}ms max wait]"


class ModelParameters(NamedTuple):
    req_duration: int
    threads: int = 1
    sla: int = 1

    def __str__(self) -> str:
        return f"Model: [{self.req_duration}ms reqs, " \
               f"{self.threads} threads, {self.sla}ms SLA]"
