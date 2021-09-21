from typing import NamedTuple


class SimulationParameters(NamedTuple):
    request_duration_ms: int
    requests_per_day: int
    max_wait: int = 1
