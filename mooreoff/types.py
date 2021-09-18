import datetime
from typing import NamedTuple


class SimulationParameters(NamedTuple):
    request_duration_ms: int
    requests_per_day: int
    simulation_length: datetime.timedelta
