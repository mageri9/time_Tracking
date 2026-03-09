import time
from dataclasses import dataclass, field
from typing import List


@dataclass
class StopwatchState:
    """Состояние секундомера (без привязки к GUI)."""

    running: bool = False
    start_time: float = 0.0
    elapsed_time: float = 0.0
    saved_time: float = 0.0
    laps: List[float] = field(default_factory=list)

    @property
    def current_time(self) -> float:
        """Текущее время с учётом паузы/старта."""
        return time.time() - self.start_time if self.running else self.elapsed_time

    @property
    def has_saved_time(self) -> bool:
        return self.saved_time != 0.0

    @property
    def has_laps(self) -> bool:
        return bool(self.laps)

